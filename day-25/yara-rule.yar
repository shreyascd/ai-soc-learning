rule Suspicious_Binary_Execution {
    meta:
        description = "Detects suspicious binary patterns common in malware"
        author = "SOC Malware Research"
        date = "2026-07-26"
        severity = "high"
    strings:
        // Suspicious API calls
        $api1 = "WinExec" ascii
        $api2 = "CreateRemoteThread" ascii
        $api3 = "VirtualAllocEx" ascii
        
        // Suspicious strings
        $str1 = "cmd.exe /c" ascii
        $str2 = "powershell.exe -enc" ascii
        $str3 = /C2[_-]?[Ss]erver[:=]\s*[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/ 
        
        // Suspicious binary signatures (process injection pattern)
        $bin1 = {48 8D 15 ?? ?? ?? ?? 48 8D 0D ?? ?? ?? ??}
        
        // Suspicious file operations
        $file1 = "\\System32\\drivers\\etc\\hosts" ascii
    condition:
        (
            ($api1 and ($api2 or $api3)) or
            ($str1 and $str2) or
            ($str3) or
            ($bin1 and $file1)
        )
        and filesize < 5MB  // Only match files < 5MB (reasonable for typical malware)
}
