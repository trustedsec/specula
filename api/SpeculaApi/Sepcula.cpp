// Sepcula.cpp : Implementation of CSepcula

#include "pch.h"
#include "Sepcula.h"

#define BUFFERSIZE 4096
// CSepcula

STDMETHODIMP_(HRESULT __stdcall) CSepcula::RunShell(BSTR cmd, VARIANT timeout, BSTR * result)
{
	CComBSTR errmsg{ L"Failed to run shell command" };
	HRESULT hret = S_OK;
	char outputbuffer[BUFFERSIZE];
	CComBSTR totaloutput{};
	DWORD availBytes = 0;
	SECURITY_ATTRIBUTES saAttr;
	saAttr.nLength = sizeof(SECURITY_ATTRIBUTES);
	saAttr.bInheritHandle = TRUE;
	saAttr.lpSecurityDescriptor = NULL;

	HANDLE hChildStd_OUT_Rd = NULL;
	HANDLE hChildStd_OUT_Wr = NULL;

	// Create a pipe for the child process's STDOUT.
	if (!CreatePipe(&hChildStd_OUT_Rd, &hChildStd_OUT_Wr, &saAttr, 0))
	{
		hret = HRESULT_FROM_WIN32(GetLastError());
		errmsg.CopyTo(result);
		return hret;
	}
	// Ensure the read handle to the pipe for STDOUT is not inherited.
	if (!SetHandleInformation(hChildStd_OUT_Rd, HANDLE_FLAG_INHERIT, 0))
	{
		CloseHandle(hChildStd_OUT_Rd);
		CloseHandle(hChildStd_OUT_Wr);
		hret = HRESULT_FROM_WIN32(GetLastError());
		errmsg.CopyTo(result);
		return hret;
	}
	STARTUPINFO siStartInfo;
	ZeroMemory(&siStartInfo, sizeof(STARTUPINFO));
	siStartInfo.cb = sizeof(STARTUPINFO);
	siStartInfo.hStdError = hChildStd_OUT_Wr;
	siStartInfo.hStdOutput = hChildStd_OUT_Wr;
	siStartInfo.dwFlags |= STARTF_USESTDHANDLES;

	PROCESS_INFORMATION piProcInfo;
	ZeroMemory(&piProcInfo, sizeof(PROCESS_INFORMATION));
	CComBSTR fullcmd{ CmdProg };
	fullcmd.Append(cmd);
	// Create the child process.
	if (!CreateProcessW(NULL,
		fullcmd,     // command line 
		NULL,                    // process security attributes 
		NULL,                    // primary thread security attributes 
		TRUE,                    // handles are inherited 
		0,                       // creation flags 
		NULL,                    // use parent's environment 
		NULL,                    // use parent's current directory 
		&siStartInfo,            // STARTUPINFO pointer 
		&piProcInfo))            // receives PROCESS_INFORMATION 
	{
		hret = HRESULT_FROM_WIN32(GetLastError());
		errmsg.CopyTo(result);
		CloseHandle(hChildStd_OUT_Rd);
		CloseHandle(hChildStd_OUT_Wr);
		return hret;
	}
	DWORD iterations = (timeout.vt == VT_I4) ? timeout.iVal : 60;
	while (WaitForSingleObject(piProcInfo.hProcess, 1000) == WAIT_TIMEOUT && iterations)
	{
		availBytes = 0;
		PeekNamedPipe(hChildStd_OUT_Rd, NULL, 0, NULL, &availBytes, NULL);
		while (availBytes)
		{
			ZeroMemory(outputbuffer, sizeof(outputbuffer));
			DWORD thisread = (availBytes >= BUFFERSIZE) ? BUFFERSIZE : availBytes;
			DWORD read = 0;
			ReadFile(hChildStd_OUT_Rd, (char*)outputbuffer, BUFFERSIZE, &read, NULL);
			totaloutput.Append(outputbuffer);
			availBytes -= read;
		}
		iterations--;
	}
	if (iterations == 0)
	{
		totaloutput.Append(L"\n\nProcess wait timed out");
	}
	else
	{
		availBytes = 0;
		PeekNamedPipe(hChildStd_OUT_Rd, NULL, 0, NULL, &availBytes, NULL);
		while (availBytes)
		{
			ZeroMemory(outputbuffer, sizeof(outputbuffer));
			DWORD thisread = (availBytes >= BUFFERSIZE) ? BUFFERSIZE : availBytes;
			DWORD read = 0;
			ReadFile(hChildStd_OUT_Rd, (char*)outputbuffer, BUFFERSIZE, &read, NULL);
			totaloutput.Append(outputbuffer);
			availBytes -= read;
		}
	}


	totaloutput.CopyTo(result);
	CloseHandle(hChildStd_OUT_Rd);
	CloseHandle(hChildStd_OUT_Wr);
	return hret;
}

STDMETHODIMP_(HRESULT __stdcall) CSepcula::LoadDll(BSTR path, boolean persist, boolean* status)
{
	HMODULE mod = LoadLibraryW(path);
	*status = false;
	if (mod == nullptr)
	{

		return HRESULT_FROM_WIN32(GetLastError());
	}
	if (!persist)
	{
		FreeLibrary(mod);
	}
	*status = true;
	return S_OK;
}
