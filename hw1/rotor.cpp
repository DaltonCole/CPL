// -*- mode: c++ -*-
/**
 * \file rotor.cpp
 *
 * \brief Defines the Rotor class
 *
 * Provides a Rotor class that acts as a rotor in V.I.L.E.'s
 * super secret encryption scheme
 */
#include "rotor.h"

Rotor::Rotor(int num)
{
  // Save for when we need to decrypt
  disk = num;

  // Initial shift value
  previous_input = 'A';
}

char Rotor::shift(char input)
{
  return (input + previous_input - 130) % 26 + 65;
}

char Rotor::decrypt(char input)
{
  char shifted = shift(input);
  char output;

  // Switch based on the disk that we're using. We only need to
  // perform that one.
  switch (disk)
  {
  case 1:
    output = decrypt_disk1(shifted);
    break;
  case 2:
    output = decrypt_disk2(shifted);
    break;
  case 3:
    output = decrypt_disk3(shifted);
    break;
  case 4:
    output = decrypt_disk4(shifted);
    break;
  case 5:
    output = decrypt_disk5(shifted);
    break;
  }

  // Record this, the most recently decrypted input, as our previous
  // input. We need it to shift later.
  previous_input = input;

  return output;
}

char Rotor::decrypt_disk1(char input)
{
  return (input + 3) % 26 + 65;
}

char Rotor::decrypt_disk2(char input)
{
  return (input + 17) % 26 + 65;
}

char Rotor::decrypt_disk3(char input)
{
  char output;
  switch (input)
  {
  case 'A':
    output = 'H';
    break;
  case 'B':
    output = 'U';
    break;
  case 'C':
    output = 'I';
    break;
  // Changed this case. Changed the 'V' to a 'P' in order to fix the decryption. This was caluclated based off of the shift function.
  case 'D':
    output = 'P';
    break;
  case 'E':
    output = 'N';
    break;
  case 'F':
    output = 'W';
    break;
  case 'G':
    output = 'C';
    break;
  case 'H':
    output = 'K';
    break;
  case 'I':
    output = 'E';
    break;
  case 'J':
    output = 'X';
    break;
  case 'K':
    output = 'Q';
    break;
  case 'L':
    output = 'Z';
    break;
  case 'M':
    output = 'O';
    break;
  case 'N':
    output = 'V';
    break;
  case 'O':
    output = 'S';
    break;
  case 'P':
    output = 'B';
    break;
  case 'Q':
    output = 'L';
    break;
  case 'R':
    output = 'J';
    break;
  case 'S':
    output = 'D';
    break;
  case 'T':
    output = 'Y';
    break;
  case 'U':
    output = 'F';
    break;
  case 'V':
    output = 'R';
    break;
  case 'W':
    output = 'A';
    break;
  case 'X':
    output = 'G';
    break;
  case 'Y':
    output = 'T';
    break;
  case 'Z':
    output = 'M';
    break;
  }

  return output;
}

char Rotor::decrypt_disk4(char input)
{
  return input % 2 ? input + 1 : input - 1;
}

char Rotor::decrypt_disk5(char input)
{
  char output;

  if (input == 'A')
  {
    output = input;
  }
  else if (input == 'Z')
  {
    output = 'B';
  }
  else if (input % 3 == 0)
  {
    output = input + 3;
  }
  else if (input % 3 == 1)
  {
    output = input + 1;
  }
  else if (input % 3 == 2)
  {
    output = input - 1;
  }

  return output;
}
