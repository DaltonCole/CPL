// -*- mode: cpp -*-
// g++ main.cpp -lboost_unit_test_framework

#define BOOST_TEST_DYN_LINK
#define BOOST_TEST_MODULE DecryptorTest
#include <boost/test/unit_test.hpp>
#include "rotor.h"
#include "funcs.h"

/**
 * Test that a Rotor will decrypt letters correctly when using disk 1
 */
BOOST_AUTO_TEST_CASE(test_disk1)
{
   // Create a test class
   Rotor rot(1);   

   // Check each decryption such that the following is true: 
   // KBLCMDNEOFPGQHRISJTKULVMWN = ABCDEFGHIJKLMNOPQRSTUVWXYZ
   BOOST_CHECK(rot.decrypt('K') == 'A');
   BOOST_CHECK(rot.decrypt('B') == 'B');
   BOOST_CHECK(rot.decrypt('L') == 'C');
   BOOST_CHECK(rot.decrypt('C') == 'D');
   BOOST_CHECK(rot.decrypt('M') == 'E');
   BOOST_CHECK(rot.decrypt('D') == 'F');
   BOOST_CHECK(rot.decrypt('N') == 'G');
   BOOST_CHECK(rot.decrypt('E') == 'H');
   BOOST_CHECK(rot.decrypt('O') == 'I');
   BOOST_CHECK(rot.decrypt('F') == 'J');
   BOOST_CHECK(rot.decrypt('P') == 'K');
   BOOST_CHECK(rot.decrypt('G') == 'L');
   BOOST_CHECK(rot.decrypt('Q') == 'M');
   BOOST_CHECK(rot.decrypt('H') == 'N');
   BOOST_CHECK(rot.decrypt('R') == 'O');
   BOOST_CHECK(rot.decrypt('I') == 'P');
   BOOST_CHECK(rot.decrypt('S') == 'Q');
   BOOST_CHECK(rot.decrypt('J') == 'R');
   BOOST_CHECK(rot.decrypt('T') == 'S');
   BOOST_CHECK(rot.decrypt('K') == 'T');
   BOOST_CHECK(rot.decrypt('U') == 'U');
   BOOST_CHECK(rot.decrypt('L') == 'V');
   BOOST_CHECK(rot.decrypt('V') == 'W');
   BOOST_CHECK(rot.decrypt('M') == 'X');
   BOOST_CHECK(rot.decrypt('W') == 'Y');
   BOOST_CHECK(rot.decrypt('N') == 'Z');
}

/**
 * Test that a Rotor will decrypt letters correctly when using disk 2
 */
BOOST_AUTO_TEST_CASE(test_disk2)
{
   // Create a test class
   Rotor rot(2);   

   // Check each decryption such that the following is true: 
   // WBXCYDZEAFBGCHDIEJFKGLHMIN == ABCDEFGHIJKLMNOPQRSTUVWXYZ
   BOOST_CHECK(rot.decrypt('W') == 'A');
   BOOST_CHECK(rot.decrypt('B') == 'B');
   BOOST_CHECK(rot.decrypt('X') == 'C');
   BOOST_CHECK(rot.decrypt('C') == 'D');
   BOOST_CHECK(rot.decrypt('Y') == 'E');
   BOOST_CHECK(rot.decrypt('D') == 'F');
   BOOST_CHECK(rot.decrypt('Z') == 'G');
   BOOST_CHECK(rot.decrypt('E') == 'H');
   BOOST_CHECK(rot.decrypt('A') == 'I');
   BOOST_CHECK(rot.decrypt('F') == 'J');
   BOOST_CHECK(rot.decrypt('B') == 'K');
   BOOST_CHECK(rot.decrypt('G') == 'L');
   BOOST_CHECK(rot.decrypt('C') == 'M');
   BOOST_CHECK(rot.decrypt('H') == 'N');
   BOOST_CHECK(rot.decrypt('D') == 'O');
   BOOST_CHECK(rot.decrypt('I') == 'P');
   BOOST_CHECK(rot.decrypt('E') == 'Q');
   BOOST_CHECK(rot.decrypt('J') == 'R');
   BOOST_CHECK(rot.decrypt('F') == 'S');
   BOOST_CHECK(rot.decrypt('K') == 'T');
   BOOST_CHECK(rot.decrypt('G') == 'U');
   BOOST_CHECK(rot.decrypt('L') == 'V');
   BOOST_CHECK(rot.decrypt('H') == 'W');
   BOOST_CHECK(rot.decrypt('M') == 'X');
   BOOST_CHECK(rot.decrypt('I') == 'Y');
   BOOST_CHECK(rot.decrypt('N') == 'Z');


}

/**
 * Test that a Rotor will decrypt letters correctly when using disk 3
 */
BOOST_AUTO_TEST_CASE(test_disk3)
{
   // Create a test class
   Rotor rot(3);   

   // Check each decryption such that the following is true: 
   // WTNFDRGUIJYSHXPOWZPJSVKZUR == ABCDEFGHIJKLMNOPQRSTUVWXYZ
   BOOST_CHECK(rot.decrypt('W') == 'A');
   BOOST_CHECK(rot.decrypt('T') == 'B');
   BOOST_CHECK(rot.decrypt('N') == 'C');
   BOOST_CHECK(rot.decrypt('F') == 'D');
   BOOST_CHECK(rot.decrypt('D') == 'E');
   BOOST_CHECK(rot.decrypt('R') == 'F');
   BOOST_CHECK(rot.decrypt('G') == 'G');
   BOOST_CHECK(rot.decrypt('U') == 'H');
   BOOST_CHECK(rot.decrypt('I') == 'I');
   BOOST_CHECK(rot.decrypt('J') == 'J');
   BOOST_CHECK(rot.decrypt('Y') == 'K');
   BOOST_CHECK(rot.decrypt('S') == 'L');
   BOOST_CHECK(rot.decrypt('H') == 'M');
   BOOST_CHECK(rot.decrypt('X') == 'N');
   BOOST_CHECK(rot.decrypt('P') == 'O');
   BOOST_CHECK(rot.decrypt('O') == 'P');
   BOOST_CHECK(rot.decrypt('W') == 'Q');
   BOOST_CHECK(rot.decrypt('Z') == 'R');
   BOOST_CHECK(rot.decrypt('P') == 'S');
   BOOST_CHECK(rot.decrypt('J') == 'T');
   BOOST_CHECK(rot.decrypt('S') == 'U');
   BOOST_CHECK(rot.decrypt('V') == 'V');
   BOOST_CHECK(rot.decrypt('K') == 'W');
   BOOST_CHECK(rot.decrypt('Z') == 'X');
   BOOST_CHECK(rot.decrypt('U') == 'Y');
   BOOST_CHECK(rot.decrypt('R') == 'Z');
}

/**
 * Test that a Rotor will decrypt letters correctly when using disk 4
 */
BOOST_AUTO_TEST_CASE(test_disk4)
{
   // Create a test class
   Rotor rot(4);   

   // Check each decryption such that the following is true: 
   // BZEYHXKWNVQUTTWSZRCQFPIOLN = ABCDEFGHIJKLMNOPQRSTUVWXYZ
   BOOST_CHECK(rot.decrypt('B') == 'A');
   BOOST_CHECK(rot.decrypt('Z') == 'B');
   BOOST_CHECK(rot.decrypt('E') == 'C');
   BOOST_CHECK(rot.decrypt('Y') == 'D');
   BOOST_CHECK(rot.decrypt('H') == 'E');
   BOOST_CHECK(rot.decrypt('X') == 'F');
   BOOST_CHECK(rot.decrypt('K') == 'G');
   BOOST_CHECK(rot.decrypt('W') == 'H');
   BOOST_CHECK(rot.decrypt('N') == 'I');
   BOOST_CHECK(rot.decrypt('V') == 'J');
   BOOST_CHECK(rot.decrypt('Q') == 'K');
   BOOST_CHECK(rot.decrypt('U') == 'L');
   BOOST_CHECK(rot.decrypt('T') == 'M');
   BOOST_CHECK(rot.decrypt('T') == 'N');
   BOOST_CHECK(rot.decrypt('W') == 'O');
   BOOST_CHECK(rot.decrypt('S') == 'P');
   BOOST_CHECK(rot.decrypt('Z') == 'Q');
   BOOST_CHECK(rot.decrypt('R') == 'R');
   BOOST_CHECK(rot.decrypt('C') == 'S');
   BOOST_CHECK(rot.decrypt('Q') == 'T');
   BOOST_CHECK(rot.decrypt('F') == 'U');
   BOOST_CHECK(rot.decrypt('P') == 'V');
   BOOST_CHECK(rot.decrypt('I') == 'W');
   BOOST_CHECK(rot.decrypt('O') == 'X');
   BOOST_CHECK(rot.decrypt('L') == 'Y');
   BOOST_CHECK(rot.decrypt('N') == 'Z');
}

/**
 * Test that a Rotor will decrypt letters correctly when using disk 5
 */
BOOST_AUTO_TEST_CASE(test_disk5)
{
   // Create a test class
   Rotor rot(5);   

   // Check each decryption such that the following is true: 
   // AZEYDDCCHBGGFFKEJJIINHMMLL = ABCDEFGHIJKLMNOPQRSTUVWXYZ
   BOOST_CHECK(rot.decrypt('A') == 'A');
   BOOST_CHECK(rot.decrypt('Z') == 'B');
   BOOST_CHECK(rot.decrypt('E') == 'C');
   BOOST_CHECK(rot.decrypt('Y') == 'D');
   BOOST_CHECK(rot.decrypt('D') == 'E');
   BOOST_CHECK(rot.decrypt('D') == 'F');
   BOOST_CHECK(rot.decrypt('C') == 'G');
   BOOST_CHECK(rot.decrypt('C') == 'H');
   BOOST_CHECK(rot.decrypt('H') == 'I');
   BOOST_CHECK(rot.decrypt('B') == 'J');
   BOOST_CHECK(rot.decrypt('G') == 'K');
   BOOST_CHECK(rot.decrypt('G') == 'L');
   BOOST_CHECK(rot.decrypt('F') == 'M');
   BOOST_CHECK(rot.decrypt('F') == 'N');
   BOOST_CHECK(rot.decrypt('K') == 'O');
   BOOST_CHECK(rot.decrypt('E') == 'P');
   BOOST_CHECK(rot.decrypt('J') == 'Q');
   BOOST_CHECK(rot.decrypt('J') == 'R');
   BOOST_CHECK(rot.decrypt('I') == 'S');
   BOOST_CHECK(rot.decrypt('I') == 'T');
   BOOST_CHECK(rot.decrypt('N') == 'U');
   BOOST_CHECK(rot.decrypt('H') == 'V');
   BOOST_CHECK(rot.decrypt('M') == 'W');
   BOOST_CHECK(rot.decrypt('M') == 'X');
   BOOST_CHECK(rot.decrypt('L') == 'Y');
   BOOST_CHECK(rot.decrypt('L') == 'Z');
}

/**
 * Test that a decrypt_message will decrypt letters correctly when using three disks
 */
BOOST_AUTO_TEST_CASE(test_decrypt_message)
{
   // Test the decryption fuction that uses three disks to compute
   BOOST_CHECK(decrypt_message(1, 2, 3, "EKY_ONHQJ_RLDEE_ZFZ_MVLFD_JEYM_WKK_SMVM_ROC") == "THE_QUICK_BROWN_FOX_JUMPS_OVER_THE_LAZY_DOG");
   BOOST_CHECK(decrypt_message(3, 4, 5, "VYO_QKSFZ_ZWQGV_POJ_IBBRB_WEWR_EHS_DZWE_JFR") == "THE_QUICK_BROWN_FOX_JUMPS_OVER_THE_LAZY_DOG");
}
