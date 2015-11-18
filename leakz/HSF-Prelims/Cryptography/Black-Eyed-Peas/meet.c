/* Written by Dmitry Chestnykh. Public domain. */
#include <err.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <openssl/blowfish.h>
#include <openssl/lhash.h>

/* Encryption and decryption */

void
cipher(int what, uint8_t *dst, uint8_t *src, uint8_t key)
{
	BF_KEY bk;

	BF_set_key(&bk, 1, &key);
	BF_ecb_encrypt(src, dst, &bk, what);
}

void
double_encrypt(uint8_t *dst, uint8_t *src, uint8_t key[2])
{
	cipher(BF_ENCRYPT, dst, src, key[0]);
	cipher(BF_ENCRYPT, dst, dst, key[1]);
}


/* Attacks */

const char report[]   = "Key: \"%c%c\"\tOperations: %d\n";
const char notfound[] = "No keys founds in %d operations\n";

/*
 * Bruteforce attack 
 */

void
bruteforce(uint8_t *plaintext, uint8_t *ciphertext)
{
	uint8_t buf1[8], buf2[8];
	int i, j, op = 0;

	for (i = 0; i < 256; i++) {
		cipher(BF_DECRYPT, buf1, ciphertext, i);
		for (j = 0; j < 256; j++) {
			++op;
			cipher(BF_DECRYPT, buf2, buf1, j);
			if (memcmp(buf2, plaintext, 8) == 0) {
				printf(report, j, i, op);
				return;
			}
		}
	}
	printf(notfound, op);
}

/* 
 * Meet-in-the-middle attack 
 */

/* Hash table of encrypted texts mapped to all possible keys */
typedef struct {
	uint8_t	enc[8]; /* encrypted text, hash table key */
	uint8_t	key;    /* 8-bit encryption key */
} EK;

/* EK_hash works reliably only if long is 64 bits */
unsigned long EK_hash(const EK *v) { return *(unsigned long *)v->enc; }
static IMPLEMENT_LHASH_HASH_FN(EK_hash, const EK*);

int EK_cmp(const EK *v1, const EK *v2) { return memcmp(v1->enc, v2->enc, 8); }
static IMPLEMENT_LHASH_COMP_FN(EK_cmp, const EK*);

void
encrypt_all_keys(LHASH *h, EK items[], uint8_t *plaintext)
{
	int i;

	for (i = 0; i < 256; i++) {
		items[i].key = i;
		cipher(BF_ENCRYPT, items[i].enc, plaintext, i);
		lh_insert(h, &items[i]);
	}
}

void
meetinthemiddle(uint8_t *plaintext, uint8_t *ciphertext)
{
	EK items[256], lookup, *found;
	LHASH *h;
	int i;

	if ((h = lh_new(LHASH_HASH_FN(EK_hash),
			LHASH_COMP_FN(EK_cmp))) == NULL) {
		warn("hash table");
		return;
	}
	encrypt_all_keys(h, items, plaintext);

	for (i = 0; i < 256; i++) {
		cipher(BF_DECRYPT, lookup.enc, ciphertext, i);
		if ((found = lh_retrieve(h, &lookup)) != NULL) {
			printf(report, found->key, i, i+256);
			goto done;
		}
	}
	printf(notfound, i+256);
done:
	lh_free(h);
}

#define	MEASURE(x) do {                                              \
	printf("%s\n", #x);                                          \
	clock_t t = clock(); (x);                                    \
	printf("%.3f sec\n\n", (clock()-t)/(double)CLOCKS_PER_SEC);  \
} while (0)

int
main()
{
	uint8_t plaintext[8] = "Dear Bob";
	uint8_t key[2] = "Go";
	uint8_t ciphertext[8];
	
	double_encrypt(ciphertext, plaintext, key);

	MEASURE( bruteforce(plaintext, ciphertext)      );
	MEASURE( meetinthemiddle(plaintext, ciphertext) );

	return 0;
}
