// -*- mode: c++ -*-
/**
 * \file rotor.h
 *
 * \brief Defines the Rotor class
 *
 * Provides a Rotor class that acts as a rotor in V.I.L.E.'s
 * super secret encryption scheme
 */
#ifndef ROTOR_H
#define ROTOR_H
#include <iostream>

using namespace std;

/**
 * A decryption rotor.
 *
 * The decryption process maintains a **shift** value that is changed
 * each time the rotor processes a letter. This means that if you want
 * to start processing a new message, you need to call `clear_shift`
 * to tell the Rotor to reset its shift value.
 */
class Rotor
{
public:
  /**
   * Disk-based constructor.
   *
   * Provide an disk number (1-5) for this rotor to use when
   * decrypting messages.
   *
   * \param num The disk number. Must be an integer 1 - 5 (inclusive)
   */
  Rotor(int num);

  /**
   * Decrypt a character.
   *
   * Decrypts a character according to the disk that this Rotor was
   * setup to use. Decrypting a character modifies the Rotor's shift
   * value, so that it is ready to process the next character in a
   * message.
   *
   * \param input The character to decrypt.
   *              Must be a captital letter A - Z (inclusive).
   */
  char decrypt(char input);

  /**
   * Clears the Rotor's shift value.
   *
   * Clears out the Rotor's shift value in order to process a new
   * message. Note that you *only* want to clear the shift value if
   * you're starting a new MESSAGE.
   *
   * Each decrypted letter depends on the previously decrypted
   * letter. Don't clear the shift value unless youre procesing an
   * entirely new message.
   */
  void clear_shift();

private:
  /**
   * Shift the input.
   *
   * Returns the input value after it has been shifted by the shift
   * value (previous_input).
   */
  char shift(char input);

  /**
   * Decrypt with disk 1 (after shift).
   */
  char decrypt_disk1(char input);

  /**
   * Decrypt with disk 2 (after shift).
   */
  char decrypt_disk2(char input);

  /**
   * Decrypt with disk 3 (after shift).
   */
  char decrypt_disk3(char input);

  /**
   * Decrypt with disk 4 (after shift).
   */
  char decrypt_disk4(char input);

  /**
   * Decrypt with disk 5 (after shift).
   */
  char decrypt_disk5(char input);

  /**
   * The disk number that this rotor is using.
   */
  int disk;

  /**
   * The most recently decrypted character.
   *
   * Used for shifting.
   */
  char previous_input;
};

#endif // ROTOR_H
