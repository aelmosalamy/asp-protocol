# Animal Sound Protocol (ASP)
ASP is a reliable, secure, comprehensive protocol that allows access to text representation of animal sounds over the internet.

## Features
**Reliability:** ASP runs over TCP to benefit from TCP's reliable, connection-oriented transmission capabilities.

**Security:** ASP provides secure animal sound transmission through state-of-the-art Caesar cipher encryption.

**Comprehensiveness:** ASP provides an extensive database of animal sounds based on this [very comprehensive listing](https://en.wikipedia.org/wiki/List_of_animal_sounds).

As of today, the ASP protocol is leading animal sound protocol in the market with support for 89 animals and their sounds.

## Packet Structure
A valid ASP packet looks as follows
```
> Version:4, Reserved:28, Key:8, Method: 32, Reserved: 24

 0                   1                   2                   3  
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Version|                        Reserved                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|       Key     |                     Method                    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|               |                    Reserved                   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                     Body ... (20 bytes) ...                   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

These are the current fields supported by ASP. ASP is future-proof; our visionary engineers added features to ensure backward and forward compatibility with the forever changing scene of secure animal sound protocols.

You should be able to get the number of bits allocated to each field using the diagram above.

1. **Version:** A 4-bit integer, tells the server what version of the ASP protocol the client is using.
2. **Reserved:** There is currently two reserved slots; our veteran protocol designers decided it is for the best of the community to ensure the future-proofing of the ASP protocol while ensuring backwards-compatability. Reserved slots are ignored by the server.
3. **Key:** Rotation offset for our battle-tested, in-house caesar cipher encryption. Number should be between 1 and 24 inclusive.
4. **Method:** A 4-byte word instructing the server to do something (More on supported methods below as they differ from version to version)
5. **Body:** A newline `\n` or null-terminated `\x00` string used by some methods.

## Behavior
**IMPORTANT:** ASP servers return all messages encrypted with the same key provided by the client. If the client loses the key it will be unable to read server messages to it.

### Version 1
ASP Version 1 is severely limited. It only supports the `CAPS` method.

### Version 2
ASP uses the battle-tested, secure Caesar Cipher algorithm for encryption using the client-provided key in some methods. These has "Encrypted." prepended to them.

In methods marked as *Encrypted*, clients must encrypt their Method using the key they provide in the same request.

The rest of the packet must remain unencrypted to ensure the server understands the request and how to decrypt it.

The server's response will also be fully encrypted using the same key to ensure confidentiality!

#### VERS
Plaintext. Returns versions supported by the server. Plaintext.

#### CAPS
*Encrypted.* Returns methods supported by the server (Since a server might not be fully supporting all methods defined in its version, non-compliant).

#### ANIM
*Encrypted.* Returns all stored animal names starting with the string in body. Case-sensitive.

#### SOUN
*Encrypted.* Returns all stored animal sounds starting with the string in body. Case-sensitive.

#### ATOS
*Encrypted.* Returns animal sound given a valid animal name as provided in body. Case-sensitive.

### Version 3
Exactly like version 2, just.... There is something special about this version.

Note, Cats are cute, but so are frogs ;)

### Errors
- ASP server received invalid packet size.
- Returns plaintext: `ASPERR: Invalid packet size.`

- ASP server gets a version it doesn't support.
- Returns plaintext: `ASPERR: Unsupported version 'x'.`

- ASP server gets a malformed packet.
- Returns plaintext: `ASPERR: Malformed packet.`

- ASP server receives an invalid key.
- Returns plaintext: `ASPERR: Invalid key 'x'`

- ASP server receives a malformed body.
- Returns encrypted: `ASPERR: Invalid body.`

- ASP server receives an animal that is not available.
- Returns encrypted: `ASPERR: Animal not found.`

