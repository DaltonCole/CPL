// -*- mode: c++ -*-
/**
 * \file funcs.h
 *
 * \brief Decryption Helper Functions
 *
 * Provides a helper function for decrypting messages that were
 * encrypted using V.I.L.E.'s super secret encryption scheme
 */
#ifndef FUNCS_H
#define FUNCS_H
#include <string>
#include <boost/algorithm/string.hpp>
#include "rotor.h"

using namespace std;
using namespace boost;

/**
 * Decrypt a message using the provided disk numbers.
 *
 * \param disk1 The disk number (1-5) to use in the LEFT rotor
 * \param disk2 The disk number (1-5) to use in the MIDDLE rotor
 * \param disk3 The disk number (1-5) to use in the RIGHT rotor
 * \param encrypted An message encrypted with the super secret
 *                  encryption scheme. Must be capital letters A-Z or
 *                  underscore. ASCII. No numbers, no whitespace.
 * \returns The decrypted message
 */
string decrypt_message(int disk1, int disk2, int disk3, string encrypted);

#endif // FUNCS_H
