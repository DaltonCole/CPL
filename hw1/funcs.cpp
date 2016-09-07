// -*- mode: c++ -*-
/**
 * \file funcs.cpp
 *
 * \brief Decryption Helper Functions
 *
 * Provides a helper function for decrypting messages that were
 * encrypted using V.I.L.E.'s super secret encryption scheme
 */
#include "funcs.h"

string decrypt_message(int disk1, int disk2, int disk3, string encrypted)
{
  Rotor left(disk1);
  Rotor middle(disk2);
  Rotor right(disk3);

  char current;

  string result = "";

  to_upper(encrypted);

  for (unsigned int i = 0; i < encrypted.length(); i++)
  {
    current = encrypted[i];

    if (current != '_')
    {
      current = left.decrypt(current);
      current = middle.decrypt(current);
      current = right.decrypt(current);
    }
    result += current;
  }

  return result;
}
