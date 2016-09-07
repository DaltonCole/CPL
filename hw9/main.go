package main

import (
	"bufio"
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"strings"
)

const (
	// NUM_GOROUTINES dictates the number of goroutines to use to
	// process data files.
	NUM_GOROUTINES = 4
)

// A Result stores results from processing a data file.
//
// Note that the Name field is the name of a **person**. Not the name
// of a file.
type Result struct {
	Name  string  // Name of the person whose data file was processed.
	Sum   float64 // The sum of all purchases made by this person
	Count int     // The total number of purchases made by this // person
}

// A Totaller can tell us the total amount of money (including taxes)
// spent in a single purchase.
type Totaller interface {
	Total() float64
}

// A SkylarkFormat stores purchase data in a format used by skylark
// birds.
type SkylarkFormat struct {
	Purchases  []float64
	TotalTaxes float64
}

type WarblerFormat struct {
	PurchaseTotal float64
}

type MynahFormat struct {
	PurchasePrice float64
	Taxes         float64
}

func (s SkylarkFormat) Total() float64 {
	var t float64

	for i := 0; i < len(s.Purchases); i++ {
		t += s.Purchases[i]
	}

	return t + s.TotalTaxes
}

func (w WarblerFormat) Total() float64 {
	return w.PurchaseTotal
}

func (m MynahFormat) Total() float64 {
	return m.PurchasePrice + m.Taxes
}

func (s *SkylarkFormat) UnmarshalJSON(data []byte) error {
	// Unmarshal a JSON object
	object := make(map[string]interface{})
	if err := json.Unmarshal(data, &object); err != nil {
		return err
	}

	// Make sure we have the "Purchases" and "TotalTaxes" fields
	// in this object.
	if _, ok := object["Purchases"]; !ok {
		return errors.New("Missing \"Purchases\" field!")
	}
	if _, ok := object["TotalTaxes"]; !ok {
		return errors.New("Missing \"TotalTaxes\" field!")
	}

	// Determine the type of the "Purchases" field.
	switch values := object["Purchases"].(type) {
	case []interface{}:
		// If the "Purchases" field is a []interface{}, which
		// it should be, iterate over its values
		for _, e := range values {
			// Determine the type of each element in the
			// []interface{}
			switch element := e.(type) {
			case float64:
				// If they're float64, then we can add
				// them to our SkylarkFormat.
				s.Purchases = append(s.Purchases, element)
			default:
				// If any item in the []interface{} is
				// NOT a float64, then we have a
				// problem.
				return errors.New("Purchases is not a []float64!")
			}
		}
	default:
		// If the "Purchases" field is not a []interface{},
		// then we have a problem.
		return errors.New("Purchases is not a []float64!")
	}

	// Determine the type of the "TotalTaxes" field.
	switch value := object["TotalTaxes"].(type) {
	case float64:
		// If it's a float64, just save it to our SkylarkFormat
		s.TotalTaxes = value
	default:
		// If it's NOT a float64, then we have a problem.
		return errors.New("TotalTaxes is not a float64!")
	}

	return nil
}

func (w *WarblerFormat) UnmarshalJSON(data []byte) error {
	// Unmarshal a JSON object
	object := make(map[string]interface{})
	if err := json.Unmarshal(data, &object); err != nil {
		return err
	}

	// Make sure we have the "PurchaseTotal" field
	if _, ok := object["PurchaseTotal"]; !ok {
		return errors.New("Missing \"PurchaseTotal\" field!")
	}

	// Determine the type of the "PurchaseTotal" field.
	switch value := object["PurchaseTotal"].(type) {
	case float64:
		w.PurchaseTotal = value
	default:
		// If not float64, we have a problem
		return errors.New("PurchaseTotal is not a float64!")
	}

	return nil
}

func (m *MynahFormat) UnmarshalJSON(data []byte) error {
	// Unmarshal a JSON object
	object := make(map[string]interface{})
	if err := json.Unmarshal(data, &object); err != nil {
		return err
	}

	// Make sure we have the "PurchasePrice" field
	if _, ok := object["PurchasePrice"]; !ok {
		return errors.New("Missing \"PurchasePrice\" field!")
	}

	// Make sure we have the "Taxes" field
	if _, ok := object["Taxes"]; !ok {
		return errors.New("Missing \"Taxes\" field!")
	}

	// Determine the type of the "PurchasePrice" field.
	switch value := object["PurchasePrice"].(type) {
	case float64:
		m.PurchasePrice = value
	default:
		// If not float64, we have a problem
		return errors.New("PurchasePrice is not a float64!")
	}

	// Determine the type of the "Taxes" field.
	switch value := object["Taxes"].(type) {
	case float64:
		m.Taxes = value
	default:
		// If not float64, we have a problem
		return errors.New("Taxes is not a float64!")
	}

	return nil
}

// unmarshalTotaller accepts a JSON-encoded object as a []byte and
// attempts to unmarshal a Totaller.
//
// It attempts to unmarshal the []byte as a WarblerFormat, then as a
// MynahFormat, then as a SkylarkFormat. If the unmarshaling for a
// type succeeds, then the unmarshaled value is returned as a
// Totaller.  If the object cannot be unmarshaled as any of the listed
// types, then the error value will be non-nil.
func unmarshalTotaller(b []byte) (Totaller, error) {
	// Variables to unmarshal values into
	var warbler WarblerFormat
	var mynah MynahFormat
	var skylark SkylarkFormat

	// Result variables
	var tot Totaller
	var err error

	// Try to unmarshal each type. If none succeed, return an
	// error. Otherwise return the value as a Totaller.
	switch {
	case json.Unmarshal(b, &warbler) == nil:
		tot = &warbler
	case json.Unmarshal(b, &mynah) == nil:
		tot = &mynah
	case json.Unmarshal(b, &skylark) == nil:
		tot = &skylark
	default:
		err = errors.New(fmt.Sprintf("Unable to unmarshal Totaller from: %q", b))
	}

	return tot, err
}

func processFile(fileName chan string, sendBack chan Result) {
	// Grab file name from channel
	fileFromChan := <-fileName

	// Open file
	file, err := os.Open(fileFromChan)
	// Make sure file opened correctly
	if err != nil {
		log.Fatalf("File failed to open")
	}
	// Close file when we exit the function
	defer file.Close()

	totalResult := Result{}

	// Scan each line for a JSON string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		// unmarshal JSON string
		tR, er := unmarshalTotaller([]byte(scanner.Text()))
		// If error, hollar
		if er != nil {
			log.Fatalf("Unmarshal failed")
		}

		// Add total to the running total of result
		totalResult.Sum += tR.Total()

		// Increase count by 1
		totalResult.Count++
	}

	// Get file name from path
	_, fName := filepath.Split(fileFromChan)

	// Get rid of extension and store file name in result's name
	totalResult.Name = strings.TrimSuffix(fName, ".dat")

	// Send results through the channel
	sendBack <- totalResult
}

func main() {
	// Set usage message
	flag.Usage = func() {
		fmt.Fprintf(os.Stderr, "Usage: %s name1.dat [name2.dat [name3.dat [...]]]\n", os.Args[0])
	}

	// Parse command line arguments
	flag.Parse()

	// Make sure that we've gotten at least one positonal argument
	if flag.NArg() < 1 {
		flag.Usage()
		os.Exit(1)
	}

	// Check that files end in ".dat"
	data_files := flag.Args()
	for _, f := range data_files {
		if !strings.HasSuffix(f, ".dat") {
			log.Fatalf("%s doesn't appear to be a data file.", f)
		}
	}

	// Create two channels, fileChan for sending, recieve for recieving
	fileChan := make(chan string)
	recieve := make(chan Result)

	// For each file, start a new process and channel file name through
	for _, f := range data_files {
		go processFile(fileChan, recieve)
		fileChan <- f
	}

	// Close fileChan
	close(fileChan)

	// stores the highest average and highest total
	var highestAverage, highestTotal Result

	// Set highest average to 999 so we do not divide by 0
	highestAverage.Count = 999

	for i := 0; i < len(data_files); i++ {
		// recieve a result from channel, and store in all
		all := <-recieve

		// Print average
		fmt.Println(fmt.Sprintf("%s spent $%.2f on average", all.Name, all.Sum/float64(all.Count)))

		// If current sum is greater than previous highest, set it to highest sum
		if all.Sum > highestTotal.Sum {
			highestTotal = all
		}
		// If current average is greater than previous averages, wet it to highest average
		if all.Sum/float64(all.Count) > highestAverage.Sum/float64(highestAverage.Count) {
			highestAverage = all
		}
	}

	// Print the highest average and sum
	fmt.Println(fmt.Sprintf("\n%s had the highest average: $%.2f", highestAverage.Name, highestAverage.Sum/float64(highestAverage.Count)))
	fmt.Println(fmt.Sprintf("%s had the highest total: $%.2f", highestTotal.Name, highestTotal.Sum))
}
