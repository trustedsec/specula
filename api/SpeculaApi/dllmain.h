// dllmain.h : Declaration of module class.

class CSpeculaApiModule : public ATL::CAtlDllModuleT< CSpeculaApiModule >
{
public :
	DECLARE_LIBID(LIBID_SpeculaApiLib)
	DECLARE_REGISTRY_APPID_RESOURCEID(IDR_SPECULAAPI, "{5be8ef76-6253-482a-926e-d1d877de3b63}")
};

extern class CSpeculaApiModule _AtlModule;
