#undef __FILE_ID__
#define __FILE_ID__ 0x02
/**
 * Dict Object Type
 *
 * Dict object type operations.
 *
 * @author      Dean Hall
 * @copyright   Copyright 2002 Dean Hall.  All rights reserved.
 * @file        dict.c
 *
 * Log:
 *
 * 2002/04/30   First.
 */

/***************************************************************
 * Includes
 **************************************************************/

#include "py.h"


/***************************************************************
 * Constants
 **************************************************************/

/***************************************************************
 * Macros
 **************************************************************/

/***************************************************************
 * Types
 **************************************************************/

/***************************************************************
 * Globals
 **************************************************************/

/***************************************************************
 * Prototypes
 **************************************************************/

/***************************************************************
 * Functions
 **************************************************************/

PyReturn_t
dict_new(pPyObj_t * r_pdict)
{
    PyReturn_t retval = PY_RET_OK;
    pPyDict_t pdict = C_NULL;

    /* allocate a dict */
    retval = heap_getChunk(sizeof(PyDict_t), (P_VOID *)r_pdict);
    PY_RETURN_IF_ERROR(retval);

    /* init dict fields */
    pdict = (pPyDict_t)*r_pdict;
    pdict->od.od_type = OBJ_TYPE_DIC;
    pdict->length = 0;
    retval = seglist_new(&pdict->d_keys);
    PY_RETURN_IF_ERROR(retval);
    retval = seglist_new(&pdict->d_vals);
    return retval;
}


PyReturn_t
dict_clear(pPyObj_t pdict)
{
    /* if null or not a dict, raise TypeError */
    if ((pdict == C_NULL) ||
        (pdict->od.od_type != OBJ_TYPE_DIC))
    {
        return PY_RET_EX_TYPE;
    }

    /* clear length */
    ((pPyDict_t)pdict)->length = 0;

    /* clear the keys and values seglists if needed */
    if (((pPyDict_t)pdict)->d_keys != C_NULL)
    {
        seglist_clear(((pPyDict_t)pdict)->d_keys);
        seglist_clear(((pPyDict_t)pdict)->d_vals);
    }
    return PY_RET_OK;
}


/*
 * Sets a value in the dict using the given key.
 *
 * Scans dict for the key.  If key val found, replace old
 * with new val.  If no key found, add key/val pair to dict.
 */
PyReturn_t
dict_setItem(pPyObj_t pdict, pPyObj_t pkey, pPyObj_t pval)
{
    PyReturn_t retval = PY_RET_OK;
    S8 segnum = 0;
    S8 indx = 0;

    /* if null parms, raise SystemError */
    if ((pdict == C_NULL)
        || (pkey == C_NULL)
        || (pval == C_NULL))
    {
        return PY_RET_EX_SYS;
    }

    /* if it's not a dict, raise TypeError */
    if (pdict->od.od_type != OBJ_TYPE_DIC)
    {
        return PY_RET_EX_TYPE;
    }
    
    /* XXX if key is not hashable, raise TypeError */
    /* XXX if key's hash hasn't been calculated */

    /* check for matching key */
    retval = seglist_findEqual(((pPyDict_t)pdict)->d_keys,
                               pkey,
                               &segnum,
                               &indx);

    /* if found a matching key, replace val obj */
    if (retval == PY_RET_OK)
    {
        retval = seglist_setItem(((pPyDict_t)pdict)->d_vals,
                                 pval,
                                 segnum,
                                 indx);
        PY_RETURN_IF_ERROR(retval);
        /* incr length */
        ((pPyDict_t)pdict)->length++;
        return PY_RET_OK;
    }

    /* if no matching key, insert the key,val pair */
    if (retval == PY_RET_NO)
    {
        retval = seglist_insertItem(((pPyDict_t)pdict)->d_keys,
                                    pkey,
                                    0,
                                    0);
        /* XXX if error here, dict might be hosed */
        PY_RETURN_IF_ERROR(retval);
        retval = seglist_insertItem(((pPyDict_t)pdict)->d_vals,
                                    pval,
                                    0,
                                    0);
        PY_RETURN_IF_ERROR(retval);
        /* incr length */
        ((pPyDict_t)pdict)->length++;
        return PY_RET_OK;
    }
    return retval;
}


PyReturn_t
dict_getItem(pPyObj_t pdict, pPyObj_t pkey, pPyObj_t * r_pobj)
{
    PyReturn_t retval = PY_RET_OK;
    S8 segnum = 0;
    S8 indx = 0;

    /* if dict is null, raise SystemError */
    if (pdict == C_NULL)
    {
        return PY_RET_EX_SYS;
    }

    /* if it's not a dict, raise TypeError */
    if (pdict->od.od_type != OBJ_TYPE_DIC)
    {
        return PY_RET_EX_TYPE;
    }

    /* if dict is empty, raise KeyError */
    if (((pPyDict_t)pdict)->length <= 0)
    {
        return PY_RET_EX_KEY;
    }

    /* check for matching key */
    retval = seglist_findEqual(((pPyDict_t)pdict)->d_keys,
                               pkey,
                               &segnum,
                               &indx);
    /* if key not found, raise KeyError */
    if (retval == PY_RET_NO)
    {
        retval = PY_RET_EX_KEY;
    }
    /* return any other error */
    PY_RETURN_IF_ERROR(retval);

    /* key was found, get obj from vals */
    retval = seglist_getItem(((pPyDict_t)pdict)->d_vals,
                             segnum,
                             indx,
                             r_pobj);
    return retval;
}


/***************************************************************
 * Test
 **************************************************************/

/***************************************************************
 * Main
 **************************************************************/
