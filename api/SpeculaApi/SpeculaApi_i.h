

/* this ALWAYS GENERATED file contains the definitions for the interfaces */


 /* File created by MIDL compiler version 8.01.0628 */
/* at Mon Jan 18 21:14:07 2038
 */
/* Compiler settings for SpeculaApi.idl:
    Oicf, W1, Zp8, env=Win32 (32b run), target_arch=X86 8.01.0628 
    protocol : dce , ms_ext, c_ext, robust
    error checks: allocation ref bounds_check enum stub_data 
    VC __declspec() decoration level: 
         __declspec(uuid()), __declspec(selectany), __declspec(novtable)
         DECLSPEC_UUID(), MIDL_INTERFACE()
*/
/* @@MIDL_FILE_HEADING(  ) */



/* verify that the <rpcndr.h> version is high enough to compile this file*/
#ifndef __REQUIRED_RPCNDR_H_VERSION__
#define __REQUIRED_RPCNDR_H_VERSION__ 500
#endif

#include "rpc.h"
#include "rpcndr.h"

#ifndef __RPCNDR_H_VERSION__
#error this stub requires an updated version of <rpcndr.h>
#endif /* __RPCNDR_H_VERSION__ */

#ifndef COM_NO_WINDOWS_H
#include "windows.h"
#include "ole2.h"
#endif /*COM_NO_WINDOWS_H*/

#ifndef __SpeculaApi_i_h__
#define __SpeculaApi_i_h__

#if defined(_MSC_VER) && (_MSC_VER >= 1020)
#pragma once
#endif

#ifndef DECLSPEC_XFGVIRT
#if defined(_CONTROL_FLOW_GUARD_XFG)
#define DECLSPEC_XFGVIRT(base, func) __declspec(xfg_virtual(base, func))
#else
#define DECLSPEC_XFGVIRT(base, func)
#endif
#endif

/* Forward Declarations */ 

#ifndef __ISepcula_FWD_DEFINED__
#define __ISepcula_FWD_DEFINED__
typedef interface ISepcula ISepcula;

#endif 	/* __ISepcula_FWD_DEFINED__ */


#ifndef __Sepcula_FWD_DEFINED__
#define __Sepcula_FWD_DEFINED__

#ifdef __cplusplus
typedef class Sepcula Sepcula;
#else
typedef struct Sepcula Sepcula;
#endif /* __cplusplus */

#endif 	/* __Sepcula_FWD_DEFINED__ */


/* header files for imported files */
#include "oaidl.h"
#include "ocidl.h"
#include "shobjidl.h"

#ifdef __cplusplus
extern "C"{
#endif 


#ifndef __ISepcula_INTERFACE_DEFINED__
#define __ISepcula_INTERFACE_DEFINED__

/* interface ISepcula */
/* [unique][nonextensible][dual][uuid][object] */ 


EXTERN_C const IID IID_ISepcula;

#if defined(__cplusplus) && !defined(CINTERFACE)
    
    MIDL_INTERFACE("b0f5f947-8064-48f7-a623-5c058dc91cc8")
    ISepcula : public IDispatch
    {
    public:
        virtual /* [id] */ HRESULT STDMETHODCALLTYPE RunShell( 
            /* [in] */ BSTR cmd,
            /* [optional][in] */ VARIANT timeout,
            /* [retval][out] */ BSTR *result) = 0;
        
        virtual /* [id] */ HRESULT STDMETHODCALLTYPE LoadDll( 
            /* [in] */ BSTR path,
            /* [in] */ boolean persist,
            /* [retval][out] */ boolean *status) = 0;
        
    };
    
    
#else 	/* C style interface */

    typedef struct ISepculaVtbl
    {
        BEGIN_INTERFACE
        
        DECLSPEC_XFGVIRT(IUnknown, QueryInterface)
        HRESULT ( STDMETHODCALLTYPE *QueryInterface )( 
            ISepcula * This,
            /* [in] */ REFIID riid,
            /* [annotation][iid_is][out] */ 
            _COM_Outptr_  void **ppvObject);
        
        DECLSPEC_XFGVIRT(IUnknown, AddRef)
        ULONG ( STDMETHODCALLTYPE *AddRef )( 
            ISepcula * This);
        
        DECLSPEC_XFGVIRT(IUnknown, Release)
        ULONG ( STDMETHODCALLTYPE *Release )( 
            ISepcula * This);
        
        DECLSPEC_XFGVIRT(IDispatch, GetTypeInfoCount)
        HRESULT ( STDMETHODCALLTYPE *GetTypeInfoCount )( 
            ISepcula * This,
            /* [out] */ UINT *pctinfo);
        
        DECLSPEC_XFGVIRT(IDispatch, GetTypeInfo)
        HRESULT ( STDMETHODCALLTYPE *GetTypeInfo )( 
            ISepcula * This,
            /* [in] */ UINT iTInfo,
            /* [in] */ LCID lcid,
            /* [out] */ ITypeInfo **ppTInfo);
        
        DECLSPEC_XFGVIRT(IDispatch, GetIDsOfNames)
        HRESULT ( STDMETHODCALLTYPE *GetIDsOfNames )( 
            ISepcula * This,
            /* [in] */ REFIID riid,
            /* [size_is][in] */ LPOLESTR *rgszNames,
            /* [range][in] */ UINT cNames,
            /* [in] */ LCID lcid,
            /* [size_is][out] */ DISPID *rgDispId);
        
        DECLSPEC_XFGVIRT(IDispatch, Invoke)
        /* [local] */ HRESULT ( STDMETHODCALLTYPE *Invoke )( 
            ISepcula * This,
            /* [annotation][in] */ 
            _In_  DISPID dispIdMember,
            /* [annotation][in] */ 
            _In_  REFIID riid,
            /* [annotation][in] */ 
            _In_  LCID lcid,
            /* [annotation][in] */ 
            _In_  WORD wFlags,
            /* [annotation][out][in] */ 
            _In_  DISPPARAMS *pDispParams,
            /* [annotation][out] */ 
            _Out_opt_  VARIANT *pVarResult,
            /* [annotation][out] */ 
            _Out_opt_  EXCEPINFO *pExcepInfo,
            /* [annotation][out] */ 
            _Out_opt_  UINT *puArgErr);
        
        DECLSPEC_XFGVIRT(ISepcula, RunShell)
        /* [id] */ HRESULT ( STDMETHODCALLTYPE *RunShell )( 
            ISepcula * This,
            /* [in] */ BSTR cmd,
            /* [optional][in] */ VARIANT timeout,
            /* [retval][out] */ BSTR *result);
        
        DECLSPEC_XFGVIRT(ISepcula, LoadDll)
        /* [id] */ HRESULT ( STDMETHODCALLTYPE *LoadDll )( 
            ISepcula * This,
            /* [in] */ BSTR path,
            /* [in] */ boolean persist,
            /* [retval][out] */ boolean *status);
        
        END_INTERFACE
    } ISepculaVtbl;

    interface ISepcula
    {
        CONST_VTBL struct ISepculaVtbl *lpVtbl;
    };

    

#ifdef COBJMACROS


#define ISepcula_QueryInterface(This,riid,ppvObject)	\
    ( (This)->lpVtbl -> QueryInterface(This,riid,ppvObject) ) 

#define ISepcula_AddRef(This)	\
    ( (This)->lpVtbl -> AddRef(This) ) 

#define ISepcula_Release(This)	\
    ( (This)->lpVtbl -> Release(This) ) 


#define ISepcula_GetTypeInfoCount(This,pctinfo)	\
    ( (This)->lpVtbl -> GetTypeInfoCount(This,pctinfo) ) 

#define ISepcula_GetTypeInfo(This,iTInfo,lcid,ppTInfo)	\
    ( (This)->lpVtbl -> GetTypeInfo(This,iTInfo,lcid,ppTInfo) ) 

#define ISepcula_GetIDsOfNames(This,riid,rgszNames,cNames,lcid,rgDispId)	\
    ( (This)->lpVtbl -> GetIDsOfNames(This,riid,rgszNames,cNames,lcid,rgDispId) ) 

#define ISepcula_Invoke(This,dispIdMember,riid,lcid,wFlags,pDispParams,pVarResult,pExcepInfo,puArgErr)	\
    ( (This)->lpVtbl -> Invoke(This,dispIdMember,riid,lcid,wFlags,pDispParams,pVarResult,pExcepInfo,puArgErr) ) 


#define ISepcula_RunShell(This,cmd,timeout,result)	\
    ( (This)->lpVtbl -> RunShell(This,cmd,timeout,result) ) 

#define ISepcula_LoadDll(This,path,persist,status)	\
    ( (This)->lpVtbl -> LoadDll(This,path,persist,status) ) 

#endif /* COBJMACROS */


#endif 	/* C style interface */




#endif 	/* __ISepcula_INTERFACE_DEFINED__ */



#ifndef __SpeculaApiLib_LIBRARY_DEFINED__
#define __SpeculaApiLib_LIBRARY_DEFINED__

/* library SpeculaApiLib */
/* [version][uuid] */ 


EXTERN_C const IID LIBID_SpeculaApiLib;

EXTERN_C const CLSID CLSID_Sepcula;

#ifdef __cplusplus

class DECLSPEC_UUID("e8b55279-c6b4-48f3-8138-b727337c0236")
Sepcula;
#endif
#endif /* __SpeculaApiLib_LIBRARY_DEFINED__ */

/* Additional Prototypes for ALL interfaces */

unsigned long             __RPC_USER  BSTR_UserSize(     unsigned long *, unsigned long            , BSTR * ); 
unsigned char * __RPC_USER  BSTR_UserMarshal(  unsigned long *, unsigned char *, BSTR * ); 
unsigned char * __RPC_USER  BSTR_UserUnmarshal(unsigned long *, unsigned char *, BSTR * ); 
void                      __RPC_USER  BSTR_UserFree(     unsigned long *, BSTR * ); 

unsigned long             __RPC_USER  VARIANT_UserSize(     unsigned long *, unsigned long            , VARIANT * ); 
unsigned char * __RPC_USER  VARIANT_UserMarshal(  unsigned long *, unsigned char *, VARIANT * ); 
unsigned char * __RPC_USER  VARIANT_UserUnmarshal(unsigned long *, unsigned char *, VARIANT * ); 
void                      __RPC_USER  VARIANT_UserFree(     unsigned long *, VARIANT * ); 

unsigned long             __RPC_USER  BSTR_UserSize64(     unsigned long *, unsigned long            , BSTR * ); 
unsigned char * __RPC_USER  BSTR_UserMarshal64(  unsigned long *, unsigned char *, BSTR * ); 
unsigned char * __RPC_USER  BSTR_UserUnmarshal64(unsigned long *, unsigned char *, BSTR * ); 
void                      __RPC_USER  BSTR_UserFree64(     unsigned long *, BSTR * ); 

unsigned long             __RPC_USER  VARIANT_UserSize64(     unsigned long *, unsigned long            , VARIANT * ); 
unsigned char * __RPC_USER  VARIANT_UserMarshal64(  unsigned long *, unsigned char *, VARIANT * ); 
unsigned char * __RPC_USER  VARIANT_UserUnmarshal64(unsigned long *, unsigned char *, VARIANT * ); 
void                      __RPC_USER  VARIANT_UserFree64(     unsigned long *, VARIANT * ); 

/* end of Additional Prototypes */

#ifdef __cplusplus
}
#endif

#endif


