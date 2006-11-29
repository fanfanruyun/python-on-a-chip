# PyMite - A flyweight Python interpreter for 8-bit microcontrollers and more.
# Copyright 2002 Dean Hall
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#

#
# Provides PyMite's builtins module, __bi.
#
# USAGE
# -----
#
# The builtins are loaded by the interpreter.
# The user must not import this module directly.
#
# LOG
# ---
#
# 2006/11/24    #26: Implement more builtin functions
# 2006/08/21    #28: Adapt native libs to use the changed func calls
# 2002/12/20    Added globals, locals, range.
# 2002/12/19    Created.
#


#### CONSTS

C = "Copyright 2002 Dean Hall.  Licensed under GPL v2."


#### FUNCS

def abs(n):
    """__NATIVE__
    pPmObj_t pn;
    pPmObj_t pm;
    int32_t n;
    PmReturn_t retval = PM_RET_OK;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Raise ValueError if arg is not int within range(256) */
    pn = NATIVE_GET_LOCAL(0);
    if (OBJ_GET_TYPE(*pn) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_VAL);
        return retval;
    }

    /* Push the absolute value onto the stack */
    n = ((pPmInt_t)pn)->val;
    if (n >= 0)
    {
        NATIVE_SET_TOS(pn);
    }
    else
    {
        retval = int_new(-n, &pm);
        NATIVE_SET_TOS(pm);
    }

    return retval;
    """
    pass


def chr(n):
    """__NATIVE__
    pPmObj_t ps;
    pPmObj_t pn;
    int32_t n;
    PmReturn_t retval;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    pn = NATIVE_GET_LOCAL(0);
    n = ((pPmInt_t)pn)->val;

    /* Raise ValueError if arg is not int within range(256) */
    if ((OBJ_GET_TYPE(*pn) != OBJ_TYPE_INT) || (n < 0) || (n > 255))

    {
        PM_RAISE(retval, PM_RET_EX_VAL);
        return retval;
    }

    /* Create char string from  integer value */
    retval = string_newFromChar((uint8_t)n, &ps);
    NATIVE_SET_TOS(ps);
    return retval;
    """
    pass


def globals():
    """__NATIVE__
    pPmObj_t pr = C_NULL;
    PmReturn_t retval;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Return calling frame's globals dict  on stack*/
    pr = (pPmObj_t)NATIVE_GET_PFRAME()->fo_globals;
    NATIVE_SET_TOS(pr);

    return PM_RET_OK;
    """
    pass


def id(o):
    """__NATIVE__
    PmReturn_t retval;
    pPmObj_t pr = C_NULL;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Return object's address as an int on the stack */
#ifdef TARGET_AVR
    retval = int_new((int32_t)(int16_t)NATIVE_GET_LOCAL(0), &pr);
#elif defined(TARGET_DESKTOP) || defined(TARGET_ARM)
    retval = int_new((int32_t)NATIVE_GET_LOCAL(0), &pr);
#else
#error Native function, __bi.id(), is not implemented for the desired target
#endif
    NATIVE_SET_TOS(pr);

    return retval;
    """
    pass


def len(s):
    """__NATIVE__
    PmReturn_t retval;
    pPmObj_t ps = C_NULL;
    pPmObj_t pr = C_NULL;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Get first arg */
    ps = NATIVE_GET_LOCAL(0);

    /* Get the length of the arg based on its type */
    switch (OBJ_GET_TYPE(*ps))
    {
        case OBJ_TYPE_STR:
            retval = int_new(((pPmString_t)ps)->length, &pr);
            break;

        case OBJ_TYPE_TUP:
            retval = int_new(((pPmTuple_t)ps)->length, &pr);
            break;

        case OBJ_TYPE_LST:
            retval = int_new(((pPmList_t)ps)->length, &pr);
            break;

        case OBJ_TYPE_DIC:
            retval = int_new(((pPmDict_t)ps)->length, &pr);
            break;

        default:
            /* If not a string or sequence type, raise TypeError */
            PM_RAISE(retval, PM_RET_EX_TYPE);
    }

    NATIVE_SET_TOS(pr);
    return retval;
    """
    pass


def locals():
    """__NATIVE__
    pPmObj_t pr = C_NULL;
    PmReturn_t retval;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Return calling frame's local attrs dict on the stack */
    pr = (pPmObj_t)NATIVE_GET_PFRAME()->fo_attrs;
    NATIVE_SET_TOS(pr);

    return PM_RET_OK;
    """
    pass


def map(f, s):
    """__NATIVE__
    PmReturn_t retval;
    pPmObj_t pf = C_NULL;
    pPmObj_t ps = C_NULL;
    pPmObj_t pr = C_NULL;
    int8_t length = 0;
    int8_t i = 0;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 2)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Get args */
    pf = NATIVE_GET_LOCAL(0);
    ps = NATIVE_GET_LOCAL(1);

    /* If args are wrong type, raise TypeError */
    if (OBJ_GET_TYPE(*pf) != OBJ_TYPE_FXN)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Get the sequence length based on type */
    switch (OBJ_GET_TYPE(*ps))
    {
        case OBJ_TYPE_TUP:
            length = ((pPmTuple_t)ps)->length;
            break;

        case OBJ_TYPE_LST:
            length = ((pPmList_t)ps)->length;
            break;

        case OBJ_TYPE_STR:
            length = ((pPmString_t)ps)->length;
            break;

        default:
            PM_RAISE(retval, PM_RET_EX_TYPE);
            return retval;
    }

    /* XXX: Do a dummy map, fill func with Nones */
    retval = list_new(&pr);
    PM_RETURN_IF_ERROR(retval);

    for (i = 0; i < length; i++)
    {
        retval = list_append(pr, PM_NONE);
        PM_RETURN_IF_ERROR(retval);
    }

    return retval;
    """
    pass


def ord(s):
    """__NATIVE__
    pPmObj_t ps;
    pPmObj_t pn;
    int32_t n;
    PmReturn_t retval;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    ps = NATIVE_GET_LOCAL(0);

    /* Raise TypeError if arg is not string of length 1 */
    if ((OBJ_GET_TYPE(*ps) != OBJ_TYPE_STR)
        || (((pPmString_t)ps)->length != 1))

    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Get integer value of character */
    n = ((pPmString_t)ps)->val[0];
    retval = int_new(n, &pn);
    NATIVE_SET_TOS(pn);
    return retval;
    """
    pass


#
# This implementation is needed by bytecodes BINARY_POWER and INPLACE_POWER
#
def pow(x, y):
    """__NATIVE__
    pPmObj_t px;
    pPmObj_t py;
    pPmObj_t pn;
    int32_t x;
    int32_t y;
    int32_t n;
    PmReturn_t retval;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 2)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    px = NATIVE_GET_LOCAL(0);
    py = NATIVE_GET_LOCAL(1);

    /* Raise TypeError if args aren't ints */
    if ((OBJ_GET_TYPE(*px) != OBJ_TYPE_INT)
        || (OBJ_GET_TYPE(*py) != OBJ_TYPE_INT))
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    x = ((pPmInt_t)px)->val;
    y = ((pPmInt_t)py)->val;

    /* Raise Value error if exponent is negative */
    if (y < 0)
    {
        PM_RAISE(retval, PM_RET_EX_VAL);
        return retval;
    }

    /* Calculate x raised to y */
    n = 1;
    while (y > 0)
    {
        n = n * x;
        y--;
    }
    retval = int_new(n, &pn);
    PM_RETURN_IF_ERROR(retval);

    /* Push result on stack */
    NATIVE_SET_TOS(pn);

    return PM_RET_OK;
    """
    pass


def range(a, b, c):
    """__NATIVE__
    PmReturn_t retval;
    pPmObj_t pa = C_NULL;
    pPmObj_t pb = C_NULL;
    pPmObj_t pc = C_NULL;
    pPmObj_t pi = C_NULL;
    pPmObj_t pr = C_NULL;
    int16_t i = 0;

    switch (NATIVE_GET_NUM_ARGS())
    {
        case 1:
            pa = PM_ZERO;
            pb = NATIVE_GET_LOCAL(0);
            pc = PM_ONE;
            break;

        case 2:
            pa = NATIVE_GET_LOCAL(0);
            pb = NATIVE_GET_LOCAL(1);
            pc = PM_ONE;
            break;

        case 3:
            pa = NATIVE_GET_LOCAL(0);
            pb = NATIVE_GET_LOCAL(1);
            pc = NATIVE_GET_LOCAL(2);

            /* If 3rd arg is 0, ValueError */
            if (((pPmInt_t)pc)->val == 0)
            {
                PM_RAISE(retval, PM_RET_EX_VAL);
                return retval;
            }
            break;

        default:
            /* If wrong number of args, raise TypeError */
            PM_RAISE(retval, PM_RET_EX_TYPE);
            return retval;
    }

    /* Allocate list */
    retval = list_new(&pr);
    PM_RETURN_IF_ERROR(retval);

    /* Iterate depending on counting direction */
    if (((pPmInt_t)pc)->val > 0)
    {
        for (i = ((pPmInt_t)pa)->val;
             i < ((pPmInt_t)pb)->val;
             i += ((pPmInt_t)pc)->val)
        {
            retval = int_new(i, &pi);
            PM_RETURN_IF_ERROR(retval);

            retval = list_append(pr, pi);
            PM_RETURN_IF_ERROR(retval);
        }
    }
    else
    {
        for (i = ((pPmInt_t)pa)->val;
             i > ((pPmInt_t)pb)->val;
             i += ((pPmInt_t)pc)->val)
        {
            retval = int_new(i, &pi);
            PM_RETURN_IF_ERROR(retval);

            retval = list_append(pr, pi);
            PM_RETURN_IF_ERROR(retval);
        }
    }

    /* Return list */
    NATIVE_SET_TOS(pr);
    return retval;
    """
    pass


def sum(s):
    """__NATIVE__
    pPmObj_t ps;
    pPmObj_t pn;
    pPmObj_t po;
    int32_t n;
    uint16_t len;
    uint16_t i;
    PmReturn_t retval;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Get the length of the sequence */
    ps = NATIVE_GET_LOCAL(0);
    if (OBJ_GET_TYPE(*ps) == OBJ_TYPE_TUP)
    {
        len = ((pPmTuple_t)ps)->length;
    }
    else if (OBJ_GET_TYPE(*ps) == OBJ_TYPE_LST)
    {
        len = ((pPmTuple_t)ps)->length;
    }
    
    /* Raise TypeError if arg is not a sequence */
    else
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Calculate the sum of the sequence */
    n = 0;
    for (i = 0; i < len; i++)
    {
        retval = seq_getSubscript(ps, i, &po);

        /* Raise TypeError if item is not an integer */
        if (OBJ_GET_TYPE(*po) != OBJ_TYPE_INT)
        {
            PM_RAISE(retval, PM_RET_EX_TYPE);
            return retval;
        }

        /* Add value to sum */
        n += ((pPmInt_t)po)->val;
    }

    retval = int_new(n, &pn);
    NATIVE_SET_TOS(pn);
    return retval;
    """
    pass


def type(o):
    """__NATIVE__
    PmReturn_t retval;
    pPmObj_t po = C_NULL;
    pPmObj_t pr = C_NULL;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Get arg */
    po = NATIVE_GET_LOCAL(0);

    /* Create int from type enum */
    retval = int_new(OBJ_GET_TYPE(*po), &pr);
    NATIVE_SET_TOS(pr);
    return retval;
    """
    pass


#
# Allocates an exception class object
#
def _exn():
    """__NATIVE__
    PmReturn_t retval;
    pPmClass_t pexn;
    uint8_t *pchunk;
    pPmObj_t pobj;

    /* Alloc a class object with attributes dict */
    retval = heap_getChunk(sizeof(PmClass_t), &pchunk);
    PM_RETURN_IF_ERROR(retval);
    pexn = (pPmClass_t)pchunk;
    OBJ_SET_TYPE(*pexn, OBJ_TYPE_EXN);
    retval = dict_new(&pobj);
    pexn->cl_attrs = (pPmDict_t)pobj;

    NATIVE_SET_TOS((pPmObj_t)pexn);

    return retval;
    """
    pass


#
# Exception classes
#
AssertionError = _exn()
AssertionError.code = 0xE4

#:mode=c:
