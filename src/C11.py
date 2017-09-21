## INFO ##
## INFO ##

#-- CHEASHEET -----------------------------------------------------------------#
# HOWTO: http://docs.sublimetext.info/en/latest/extensibility/syntaxdefs.html
# REGEX: http://www.geocities.jp/kosako3/oniguruma/doc/RE.txt

#-- C STANDARD ----------------------------------------------------------------#
# http://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf


# hexadecimal  | octal         | newline   | double-quote |
# single-quote | question-mark | bell      | backspace    |
# formfeed     | line-feed     | return    | tab          |
# vertical-tab | escape char
ESCAPED_CHARS = r'\\(x\h+|[0-7]([0-7][0-7]?)?|\n|"|\'|\?|a|b|f|n|r|t|v|\\|0)'
TRIGRAPH_SEQS = r"\?\?[=/()'<>!-]"
HEXADEC_CHARS = r'\\(u\h{4}|U\h{8})'

# Syntax Definition
syntax = {
    'name': '{NAME}',
    'comment': ('\n\t\tCopyright (C) 2015 - 2017 Peter Varo'
                '\n\t\t<http://github.com/petervaro/c11>'
                '\n\t\t<http://petervaro.com>'
                '\n'
                '\n\t\tThis program is free software: you can redistribute it'
                '\n\t\tand/or modify it under the terms of the GNU General'
                '\n\t\tPublic License as published by the Free Software'
                '\n\t\tFoundation, either version 3 of the License, or (at your'
                '\n\t\toption) any later version.'
                '\n'
                '\n\t\tThis program is distributed in the hope that it will be'
                '\n\t\tuseful, but WITHOUT ANY WARRANTY; without even the'
                '\n\t\timplied warranty of MERCHANTABILITY or FITNESS FOR A'
                '\n\t\tPARTICULAR PURPOSE. See the GNU General Public License'
                '\n\t\tfor more details.'
                '\n'
                '\n\t\tYou should have received a copy of the GNU General Public'
                '\n\t\tLicense along with this program, most likely a file in'
                '\n\t\tthe root directory, called "LICENSE". If not, see'
                '\n\t\t<http://www.gnu.org/licenses>.'
                '\n\t'),
    'scopeName': 'source.{SCOPE}',
    'fileTypes': ['c', 'h'],
    'keyEquivalent': '^~C',
    # hashbang
    'firstLineMatch': r'\b(-[*]-)(Mode:)? C \1\b',
    # Folding marks for the TextEditor
    'foldingStartMarker': r'\.*({|\()',
    'foldingStopMarker' : r'\.*(}|\))',
    # Patterns
    'patterns':
    [
#-- COMMENT -------------------------------------------------------------------#
        # TODO: At the moment tmLanguage doesn't support multiline regexes
        #       only through begin/patterns/end, which makes it impossible to
        #       catch something like this:
        #
        #          r'/(\\\s*\n)*/((\\\s*\n)?.*)*'
        #
        #       Which should produce a match on this:
        #
        #          /\
        #          / Comment: another kind of two-lines one-liner
        #
        #       This notation is a valid C syntax according to the standard.
        {
            # One-liner
            'name' : 'comment.line.double_slash.{SCOPE}',
            'begin': r'//',
            'patterns':
            [
                {
                    'name' : 'comment.line.double_slash.line_continuation.{SCOPE}',
                    'match': r'\\\s*\n'
                }
            ],
            'end': r'(?<!\\)\n'
        },
        {
            # Multi-liner
            'name' : 'comment.block.slash_star.{SCOPE}',
            'begin': r'/\*',
            'end'  : r'\*/'
        },


#-- NUMBERS -------------------------------------------------------------------#
        {
            # .001 .001f  .1e6F  .1E6  .1e+6  .1E+6  .1e-6  .1E-6
            'name' : 'constant.numeric.float_and_double_and_long_double'
                     '.decimal.pointdigit.{SCOPE}',
            'match': r'(?<=\W|^)\.\d+([eE][+-]?\d+)?[fFlL]?\b'
        },
        {
            # 1. 1.f  1.0F  1.1e6  1.1E6  1.1e+6  1.1E+6  1.1e-6  1.1E-6
            'name' : 'constant.numeric.float_and_double_and_long_double'
                     '.decimal.digitpoint.{SCOPE}',
            'match': r'(?<!\w)\d+\.(\d+([eE][+-]?\d+)?)?[fFlL]?(?=\W)'
        },

        {
            # 0xA.99p123f
            'name' : ('constant.numeric.float_and_double_and_long_double'
                      '.hexadecimal.pointdigit.{SCOPE}'),
            'match': r'\b0[xX](\h+)?\.\h*([pP][+-]?\d+)?[fFlL]?'
        },
        {
            'name' : ('constant.numericic.signed_and_unsigned_and'
                      '_long_and_long_long_integer.decimal.{SCOPE}'),
            'match': r'(?<!\.)([1-9]\d*|0)([eE][+-]?\d+)?[uU]?(ll?|LL?)?\b'
        },
        {
            # 017 001
            'name' : 'constant.numeric.integer.octal.{SCOPE}',
            'match': r'\b0[0-7]+'
        },
        {
            # 0xff 0xFF 0Xff 0XFF
            'name' : 'constant.numeric.integer.hexadecimal.{SCOPE}',
            'match': r'\b0[xX]\h+'
        },

#-- CONSTANTS -----------------------------------------------------------------#
        {
            'include': '#strong_constants'
        },
        {
            'include': '#weak_constants'
        },


#-- KEYWORDS ------------------------------------------------------------------#
        {
            'name' : 'keyword.storage.class_specifiers.{SCOPE}',
            'match': r'\b(typedef|extern|static|_Thread_local|auto|register)\b'
        },
        {
            'name' : 'keyword.type.type_qualifiers.{SCOPE}',
            'match': r'\b(const|restrict|volatile|_Atomic)\b'
        },
        {
            'name' : 'keyword.function.function_specifiers.{SCOPE}',
            'match': r'\b(inline|(_N|n)oreturn)\b'
        },
        {
            'name' : 'keyword.other.assertion.{SCOPE}',
            'match': r'\b(((_S|s)tatic_)?assert)\b'
        },
        # TODO: static-assertion keyword?
        {
            'name' : 'keyword.other.generic.{SCOPE}',
            'match': r'\b_Generic\b'
        },
        {
            'name' : 'keyword.control.jump_statements.{SCOPE}',
            'match': r'\b(break|continue|goto|return)\b'
        },
        {
            'name' : 'keyword.control.iteration_statements.{SCOPE}',
            'match': r'\b(do|while|for)\b'
        },
        {
            'name' : 'keyword.control.switch_statements.{SCOPE}',
            'match': r'\b(switch|case|default)\b'
        },
        {
            'name' : 'keyword.control.conditional_statements.{SCOPE}',
            'match': r'\b(if|else)\b'
        },
#-- OPERATORS -----------------------------------------------------------------#
        {
            'name' : 'keyword.operator.ternary.{SCOPE}',
            'match': r'\?|:'
        },
        {
            'name' : 'keyword.operator.assignment.augmented.{SCOPE}',
            'match': r'\+\+|--|(\+|-|\*|/|%|&|\^|\||<<|>>)='
        },
        {
            'name' : 'keyword.operator.comparison.{SCOPE}',
            'match': r'(<|>)=?|(=|!)='
        },
        {
            'name' : 'keyword.operator.bool.logical.{SCOPE}',
            'match': r'&&|\|\||!'
        },
        {
            'name' : 'keyword.operator.arithmetic.{SCOPE}',
            'match': r'\+|-|\*|/|%|&|\^|\||~|<<|>>|'
                     r'(size|offset)of|(_A|a)lign(as|of)'
        },
        {
            'name' : 'keyword.operator.value_and_annotation_assignment.{SCOPE}',
            'match': r'=|\.|->'
        },


#-- FUNCTION ------------------------------------------------------------------#
        # separate function declaration, definition and call ?


#-- BUILTINS ------------------------------------------------------------------#
        {
            'include': '#builtin_types'
        },
        # {
        #     'include': '#builtin_functions'
        # },


#-- ETC -----------------------------------------------------------------------#
        # {
        #     'include': '#line_continuation'
        # },
        # {
        #     'include': '#language_variables'
        # },

#-- STRUCTURES ----------------------------------------------------------------#

        # struct, enum, array?

#-- MACROS --------------------------------------------------------------------#
        {
            'include': '#macros'
        },

#-- ACCESS --------------------------------------------------------------------#
        {
            # TODO: Try to catch function-pointer before function-call. The hard
            #       part is the result type can be anything: word-like
            #       characters, built-in type (with spaces) or even a function
            #       pointer. Examples:
            #           void (*hello)()      << correct
            #           type (*hello)()      << not correct
            #           long long (*hello)() << correct
            #           void(*)()(*f)()      << correct
            'name' : 'meta.function_pointer.{SCOPE}',
            'begin': r'\(\s*(\*+)\s*([a-zA-Z_]\w*)\s*\)\s*\(',
            'beginCaptures':
            {
                1: {'name': 'keyword.operator.pointer.{SCOPE}'},
                2: {'name': 'support.function.name.{SCOPE}'}
            },
            'patterns':
            [
                {'include': '$self'}
            ],
            'end': r'\)'
        },
        {
            'name' : 'meta.function_call.{SCOPE}',
            'begin': r'([a-zA-Z_]\w*)\s*\(',
            'beginCaptures':
            {
                1: {'name': 'support.function.name.{SCOPE}'}
            },
            'patterns':
            [
                {'include': '$self'}
            ],
            'end':r'\)',
        },
        {
            'name' : 'variable.language.member_access.{SCOPE}',
            'match': r'(?<=\.|->)\s*[a-zA-Z_]\w*',
        },

#-- STRING --------------------------------------------------------------------#
        {
            'include': '#string_quoted'
        },

#-- VARIABLES -----------------------------------------------------------------#
        {
            'include': '#generic_names'
        },
    ],

#-- REPOSITORY ----------------------------------------------------------------#
    'repository':
    {

#-- CHARACTER REPLACE ---------------------------------------------------------#
        'trigraph_sequences':
        {
            'name' : 'constant.character.escaped.trigraph_sequences.{SCOPE}',
            'match': TRIGRAPH_SEQS
        },

#-- BUILTINS ------------------------------------------------------------------#
        'builtin_functions':
        {
            'name' : 'support.function.builtin.{SCOPE}',
            'match': r'is(al(num|pha)|cntrl|x?digit|graph|(low|upp)er|'
                     r'p(rin|unc)t|space)|to((low|upp)er)'
        },

        'builtin_types':
        {
            'patterns':
            [
                {
                    'name' : 'invalid.illegal.support.type.{SCOPE}',
                    'match':
                    (
                        r'(((char|int|void|float|double|(b|_B)ool)\s+){2,}|'
                        r'(_Complex(_I)?|complex|_Imaginary(_I)|imaginary)+|'
                        r'((un)?signed\s+)+((float|(long\s+)?double|void|(b|_B)ool)(\s+char)?\s+)+)'
                    )
                },
                {
                    'name' : 'support.type.{SCOPE}',
                    'match':
                    (

                        r'\b(void|(b|_B)ool|(float|(long\s+)?double)(\s+'
                            r'(_Complex(_I)?|complex|_Imaginary(_I)|imaginary))?|'
                        r'((un)?signed\s+)?(char|(short|long(\s+long)?)(\s+int)?|(int)?))\b'

                        # TODO: enum ?

                    )
                },
                {
                    'name' : 'storage.modifier.variable.type.special.{SCOPE}',
                    'match': r'\b('
                             r'FILE|va_list|lconv|once_flag|'
                             r'mtx_(plain|recursive|timed)|'
                             r'thrd_(success|nomem|timedout|busy|error)|'
                             r'(ptrdiff|r?size|wchar|fpos|l?l?div|'
                             r'char(16|32)|sig_atomic|clock|time|max_align|'
                             r'u?int((_(fast|least))?(8|16|32|64)|(max|ptr))|'
                             r'imaxdiv|fe(nv|xcept)|errno|cnd|thrd(_start)?|'
                             r'tss(_dtor)?|mtx)_t'
                             r')\b'
                },
                {
                    'name' : 'support.type.member.{SCOPE}',
                    'match': r'\b(struct|union|enum)\b'
                }
            ]
        },


#-- ENTITY --------------------------------------------------------------------#
        'entity_name_class':
        {
            'patterns':
            [
                {'include': '#illegal_names'},
                {'include': '#generic_names'}
            ]
        },
        'generic_names':
        {
            'match': r'[a-zA-Z_]\w*'
        },
        'illegal_names':
        {
            'name' : 'invalid.illegal_names.name.{SCOPE}',
            'match':
            (
                r'\b('
                r'auto|break|case|char|const|continue|default|do|double|else|'
                r'enum|extern|float|for|goto|if|inline|int|long|register|'
                r'restrict|return|short|signed|sizeof|static|struct|switch|'
                r'typedef|union|unsigned|void|volatile|while|(_A|a)lign(as|of)|'
                r'_Atomic|_Bool|_Generic|(_C|c)omplex(_I)?|(_I|i)maginary(_I)?|'
                r'_Noreturn|((_S|s)tatic_)?assert|_Thread_local'
                r')\b'
            )
        },

#-- CONSTANTS -----------------------------------------------------------------#
        'strong_constants':
        {
            'patterns':
            [

                {
                    'name' : 'constant.other.ellipsis.{SCOPE}',
                    'match': r'\.\.\.'
                },
                {
                    'name' : 'constant.language.word_like.{SCOPE}',
                    'match': r'\b(NULL|EOF|EXIT_(FAILURE|SUCCESS)|'
                             r'true|false|std(in|out|err))\b'
                }
            ]
        },
        'weak_constants':
        {
            'patterns':
            [
                {
                    'name' : 'support.variable.macro.dunder.{SCOPE}',
                    'match': r'\b__('
                             r'(LIN|FIL|DAT|TIM)E|VA_ARGS|func|'
                             r'STDC(_(HOSTED|VERSION|ISO_10646|MB_MIGHT_NEQ_WC|'
                             r'UTF_(16|32)|ANALYZABLE|IEC_559(_COMPLEX_)?|'
                             r'(WANT_)?LIB_EXT1|NO_(ATOMICS|COMPLEX|THREADS|'
                             r'VLA)))?'
                             r')__\b'
                },
                {
                    'name' : 'support.variable.macro.constant.{SCOPE}',
                    'match': r'\b('
                             r'NDEBUG|CHAR_BIT|CLOCKS_PER_SEC|'
                             r'(S?CHAR|SHRT|INT|L?LONG)_(MAX|MIN)|'
                             r'(U(CHAR|SHRT|INT|L?LONG)|MB_LEN)_MAX|'
                             r'FLT_(RADIX|ROUNDS|EVAL_METHOD)|DECIMAL_DIG|'
                             r'(FLT|L?DBL)_(((MANT|DECIMAL)_)?DIG|'
                                r'(MIN|MAX)((_(10_)?EXP))?|'
                                r'EPSILON|TRUE_MIN|HAS_SUBNORM)|'
                             r'FP_ILOGB(0|NAN)|'
                             r'FE_((OVER|UNDER)FLOW|IN(EXACT|VALID)'
                                r'|ALL_EXCEPT|DIVBYZERO|(UP|DOWN)WARD|'
                                r'TO(NEAREST|WARDZERO)|DFL_ENV)|'
                             r'LC_(ALL|COLLATE|CTYPE|MONETARY|NUMERIC|TIME)|'
                             r'BUFSIZ|(TMP|F(OPEN|ILENAME))_MAX|_IO(F|L|N)BF|'
                                r'SEEK_(CUR|END|SET)|L_tmpnam|'
                             r'SIG(ABRT|FPE|ILL|INT|SEGV|TERM|_(DFL|IGN|ERR))|'
                             r'ONCE_FLAG_INIT|TSS_DTOR_ITERATIONS'
                             r')\b'
                }
            ]
        },
        'macro_keyword':
        {
            'patterns':
            [
                {
                    'name' : 'keyword.operator.macro.conditional.{SCOPE}',
                    'match': r'\bdefined\b'
                },
                {
                    'name' : 'keyword.operator.macro.pragma.{SCOPE}',
                    'match': r'\b_Pragma\b'
                }
            ]
        },


#-- MACROS --------------------------------------------------------------------#
        'macros':
        {
            'patterns':
            [
                {
                    'name' : 'entity.other.macro.keywords.{SCOPE}',
                    'match': r'^\s*(#)\s*((include\s+(<(.+)>|"(.+)"))|'
                             r'line|error|pragma|'
                             r'(un|ifn?)def|else|endif)',
                    'captures':
                    {
                        5: {'name': 'entity.other.inherited-class.include.{SCOPE}'},
                        6: {'name': 'storage.modifier.include.{SCOPE}'}
                    }
                },
                {
                    'name' : 'meta.other.macro.define.{SCOPE}',
                    'begin': r'^\s*(#\s*define)\s+(?=[a-zA-Z_]\w*)',
                    'beginCaptures':
                    {
                        1: {'name': 'entity.other.macro.define.{SCOPE}'}
                    },
                    'patterns':
                    [
                        {
                            'contentName': 'storage.modifier.variable.{SCOPE}',
                            'begin': r'(?=[a-zA-Z_]\w*)',
                            'patterns':
                            [
                                {'include': '#strong_constants'},
                                {'include': '#weak_constants'},
                            ],
                            'end': r'(?!\w)'
                        }
                    ],
                    'end': r'\s|$\n|\W'
                },
                {
                    'name' : 'meta.other.macro.conditional.{SCOPE}',
                    'begin': r'^\s*(#\s*(el)?if)',
                    'beginCaptures':
                    {
                        1: {'name': 'entity.other.macro.conditional.{SCOPE}'}
                    },
                    'patterns':
                    [
                        {'include': '#macro_keyword'},
                        {'include': '#strong_constants'},
                        {'include': '#weak_constants'},
                        {'include': '$self'}
                    ],
                    'end': r'(?<!\\)\n'
                },
                # Macro variable concatanation
                # FIXME: #define __paste(_0,_1,_2,_3,_4) _0##_1##_2##_3##_4
                #                                             ^
                #                                  highlighted as number

                # FIXME: some_var, ## \   <-- line-breaker
                #        amother_var

                # FIXME: word##1 (number)
                {
                    'name' : 'string.interpolated.macro.concatanate.{SCOPE}',
                    'begin': r'[a-zA-Z_]\w*\s*,?\s*(##)',
                    'beginCaptures':
                    {
                        1: {'name': 'keyword.operator.macro.concatanate.{SCOPE}'}
                    },
                    'patterns':
                    [
                        {
                            'contentName': 'string.interpolated.macro.concatanate.{SCOPE}',
                            'match': r'\s*[a-zA-Z_]\w*\s*,?\s*(##)',
                            'captures':
                            {
                                1: {'name': 'keyword.operator.macro.concatanate.{SCOPE}'}
                            }
                        }
                    ],
                    'end': r'\s*[a-zA-Z_]\w*(?!\s*,?\s*(##))'
                },
                # Macro variable stringify
                {
                    'name' : 'string.interpolated.macro.stringify.{SCOPE}',
                    'match': r'(?<!^)\s*(#)\s*[a-zA-Z_]\w*',
                    'captures':
                    {
                        1: {'name': 'keyword.operator.macro.stringify.{SCOPE}'}
                    }
                }
            ]
        },

#-- STRING --------------------------------------------------------------------#
        'string_quoted':
        {
            'patterns':
            [
                # Single Quoted Char Constant
                {
                    'name' : 'string.quoted.single.trigraph.{SCOPE}',
                    'match': r"(\b[LUu])?'(" + TRIGRAPH_SEQS + r")'",
                    'captures':
                    {
                        1: {'name': 'storage.type.string.quoted.single.prefix.{SCOPE}'},
                        2: {'name': 'constant.character.escaped.trigraph_sequences.{SCOPE}'}
                    }
                },
                {
                    'name' : 'string.quoted.single.escaped.{SCOPE}',
                    'match': r"(\b[LUu])?'(" + ESCAPED_CHARS + r")'",
                    'captures':
                    {
                        1: {'name': 'storage.type.string.quoted.single.prefix.{SCOPE}'},
                        2: {'name': 'constant.character.escaped.special.{SCOPE}'}
                    }
                },
                {
                    'name' : 'string.quoted.single.hexadecimal.{SCOPE}',
                    'match': r"(\b[LUu])?'(" + HEXADEC_CHARS + r")'",
                    'captures':
                    {
                        1: {'name': 'storage.type.string.quoted.single.prefix.{SCOPE}'},
                        2: {'name': 'constant.character.escaped.{SCOPE}'}
                    }
                },
                {
                    'name' : 'string.quoted.single.illegal.{SCOPE}',
                    'match': r"(\b[LUu])?'(\\|'|\n)'",
                    'captures':
                    {
                        1: {'name': 'storage.type.string.quoted.single.prefix.{SCOPE}'},
                        2: {'name': 'invalid.illegal.string.quoted.single.{SCOPE}'}
                    }
                },
                {
                    'name' : 'string.quoted.single.regular.{SCOPE}',
                    'match': r"(\b[LUu])?'.(.*?)'",
                    'captures':
                    {
                        1: {'name': 'storage.type.string.quoted.single.prefix.{SCOPE}'},
                        2: {'name': 'invalid.illegal.string.quoted.more.{SCOPE}'}
                    }
                },


                # Double Quoted Literal Constant
                {
                    'name' : 'string.quoted.double.{SCOPE}',
                    'begin': r'(\b[LU]|u8?)?"',
                    'beginCaptures':
                    {
                        1: {'name': 'storage.type.string.quoted.single.prefix.{SCOPE}'},
                    },
                    'patterns':
                    [
                        {'include': '#trigraph_sequences'},
                        {'include': '#string_patterns'},
                        {
                            'name' : 'invalid.illegal.string.quoted.single.{SCOPE}',
                            'match': r'(\\|"|\n)',
                        },
                    ],
                    'end': r'"|(\n)',
                    'endCaptures':
                    {
                        1: {'name': 'invalid.illegal.unclosed_string.cython'}
                    }
                }
            ]
        },
        'string_patterns':
        {
            'patterns':
            [
                {'include': '#constant_placeholder'},
                {'include': '#escaped_characters'},
                {'include': '#escaped_unicode_characters'}
            ]
        },



# r"""
# (?x)%
# (\d+\$)?                             (?# field (argument #)
# [#0\- +']*                           (?# flags)
# [,;:_]?                              (?# separator character (AltiVec)
# ((-?\d+)|\*(-?\d+\$)?)?              (?# minimum field width)
# (\.((-?\d+)|\*(-?\d+\$)?)?)?         (?# precision)
# (hh|h|ll|l|j|t|z|q|L|vh|vl|v|hv|hl)? (?# length modifier)
# [diouxXDOUeEfFgGaACcSspn%]           (?# conversion type)
# """




        'constant_placeholder':
        {
            # FIXME: format prefixes: -= 0w.pmc
            'name' : 'string.interpolated.placeholder.{SCOPE}',
            'match': r'%(((ll?|t|h)?(d|i))|(ll?|z|j|h)?u|((\.\d*)?(l|L)?f)|[%csaeEoxXpngG])'
            # r'%(\(\w+\))?#?0?-?[ ]?\+?(\d*|\*)(\.(\d*|\*))?[hlLz]?[diouxXeEfFgGcrspn%]'
        },
        'escaped_characters':
        {
            'name' : 'constant.character.escaped.special.{SCOPE}',
            'match': ESCAPED_CHARS
        },
        'escaped_unicode_characters':
        {
            # 16bit hex | 32bit hex
            'name' : 'constant.character.escaped.{SCOPE}',
            'match': HEXADEC_CHARS
        }
    },
    'uuid': '8F217A3C-DD44-C9F6-8883-7FF1A89624CC'
}
