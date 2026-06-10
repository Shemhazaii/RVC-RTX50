<div align="center">
<h1>Retrieval-based-Voice-Conversion-WebUI & Real Time GUI for Nvidia RTX 40 & 50 series</h1>
</div>

------

## Summary
This repository has the following features:
+ Updated Python to 3.11
+ Updated libraries version to support latest Nvidia GPUs
+ Added one click installer for both linux and windows

## What i did not do yet
+ Still not updated for Intel or AMD gpus since i don't own any kind of GPU from these brands to test

## Preparing the environment

The following commands need to be executed in the environment of Python version 3.11 or higher.

Windows 
```bash
 install.bat
 
 #then run start.bat or start-web.bat
 start.bat
 start-web.bat
```

Windows 
```bash
 sh ./install.sh
 
 #then run start.sh or start-web.sh
 sh ./start.sh
 sh ./start-web.bat
```

required models are automatically downloaded but you might still need to download UVR5 models through [Huggingface space](https://huggingface.co/lj1995/VoiceConversionWebUI/tree/main/).

## Credits
+ [RVC PROJECT](https://github.com/RVC-Project)
+ All the credits on RVC Project
+ RVC Project Contributors

