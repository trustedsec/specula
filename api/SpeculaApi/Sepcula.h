// Sepcula.h : Declaration of the CSepcula

#pragma once
#include "resource.h"       // main symbols



#include "SpeculaApi_i.h"



using namespace ATL;


// CSepcula

class ATL_NO_VTABLE CSepcula :
	public CComObjectRootEx<CComMultiThreadModel>,
	public CComCoClass<CSepcula, &CLSID_Sepcula>,
	public IDispatchImpl<ISepcula, &IID_ISepcula, &LIBID_SpeculaApiLib, /*wMajor =*/ 1, /*wMinor =*/ 0>
{
public:
	CSepcula()
	{
	}

DECLARE_REGISTRY_RESOURCEID(IDR_SEPCULA)


BEGIN_COM_MAP(CSepcula)
	COM_INTERFACE_ENTRY(ISepcula)
	COM_INTERFACE_ENTRY(IDispatch)
END_COM_MAP()



	DECLARE_PROTECT_FINAL_CONSTRUCT()

	HRESULT FinalConstruct()
	{
		return S_OK;
	}

	void FinalRelease()
	{
	}

public:
	STDMETHOD(RunShell)(BSTR cmd, VARIANT timeout, BSTR * result);
	STDMETHOD(LoadDll)(BSTR path, boolean persist,  boolean* status);


private:
	CComBSTR CmdProg{L"C:\\Windows\\system32\\cmd.exe /c "};



};

OBJECT_ENTRY_AUTO(__uuidof(Sepcula), CSepcula)
