/* OpenSSL 4 getters return const; Squid 7.6 still stores the results in
 * mutable pointers. Unwrap after the real OpenSSL headers are visible. */
#ifdef __cplusplus
#include <openssl/x509.h>
static inline X509_NAME *
omv_X509_get_subject_name(const X509 *c)
{
	return const_cast<X509_NAME *>(::X509_get_subject_name(c));
}
static inline X509_NAME *
omv_X509_get_issuer_name(const X509 *c)
{
	return const_cast<X509_NAME *>(::X509_get_issuer_name(c));
}
static inline X509_NAME_ENTRY *
omv_X509_NAME_get_entry(const X509_NAME *n, int loc)
{
	return const_cast<X509_NAME_ENTRY *>(::X509_NAME_get_entry(n, loc));
}
static inline X509_EXTENSION *
omv_X509_get_ext(const X509 *c, int loc)
{
	return const_cast<X509_EXTENSION *>(::X509_get_ext(c, loc));
}
static inline unsigned char *
omv_X509_alias_get0(X509 *c, int *len)
{
	return const_cast<unsigned char *>(::X509_alias_get0(c, len));
}
#undef X509_get_subject_name
#undef X509_get_issuer_name
#undef X509_NAME_get_entry
#undef X509_get_ext
#undef X509_alias_get0
#define X509_get_subject_name omv_X509_get_subject_name
#define X509_get_issuer_name omv_X509_get_issuer_name
#define X509_NAME_get_entry omv_X509_NAME_get_entry
#define X509_get_ext omv_X509_get_ext
#define X509_alias_get0 omv_X509_alias_get0
#endif
