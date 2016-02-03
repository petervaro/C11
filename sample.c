// Single-line comment
// Single-line \
   multi-line  \
   comment
/* Multi-line
   comment */

#include <stdio.h>
#include <assert.h>
#include <stddef.h>
#include <stdlib.h>
#include <limits.h>

#ifdef FLAG
    #include "folder/module.h"
#endif

#define MACRO() printf("In %s, at %d, in `%s'\n", __FILE__, __LINE__, __func__)
#define CONCAT(A, B) A ## B

#if __STDC_VERSION__ < 201112L
   #error "Must be compiled with `-std=c11'"
#elif defined __STDC_NO_THREADS__
   typedef struct thrd_t_ thrd_t;
   typedef struct mtx_t_  mtx_t;
#else
   #include <threads.h>
#endif

#if !defined MACRO
   #error "`MACRO' has to be defined"
#elif !defined noreturn
   #define noreturn _Noreturn
#endif

static const float        a = .001f,
                          b = .1e6F,
                          c = .1E+6f,
                          d = .1e-6f,
                          e = 1.f,
                          f = 1.1E6f,
                          g = 0xA.99p123f;
static const int          h = 017;
static const unsigned int i = 0xDeadBeef;

noreturn
crazy_func(thrd_t *restrict p1,
           mtx_t  *restrict p2,
           ...);

int
main(int          argc,
     const char **argv)
{
    size_t   buff_size;
    void   (*function)(int, float(*)(void));

    static_assert(1 > 0, "Impossible: `1 is lesser than 0'");

    MACRO();

    printf("Number of bits in a byte: %d\n", CHAR_BIT);
    return EXIT_SUCCESS;
}
