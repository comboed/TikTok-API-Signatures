
__________________
**REQUIREMENTS**  
A rooted Android(Emulator works) or jailbroken IOS device.  
Frida and Frida-Tools  
A brain.  

To inject the script, run via shell; *http://127.0.0.1:5000/run/*

Script functions:  
  &ensp; **Sign TikTok API's**  [Usage: *http://127.0.0.1:5000/sign/?{ENDPOINT}*]  
  &ensp; **Register TikTok Devices** [Usage: *http://127.0.0.1:5000/register_device/*]  
  
 Registered devices are based on TikTok version 24.7.2 and use TikTok's infamous **TTEncrypt**.  
 Depending on the APK, will determine which version of **X-Gorgon** will be generated. Anything after 18.9.5 (v0404) will **not work**.  
 
 This script is for educational purposes and is not to be sold under any circumstances.
 
 Current Issues:  
  &ensp; Device registration will register a device, but the device/install id are **unusable** until they are XLOG'd. I currently do not have enough time on my hands to write the XLOG data.  
  
  Credits:  
  @SebastienWae  
  @coder-fly
