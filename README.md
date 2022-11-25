# Extract Android OTA Payload.bin File using Payload Dumper

#### 1. Install Python: https://www.python.org/downloads

#### 2. Download the full OTA ZIP package for your Android device. Extract the downloaded ZIP file to your PC using an archive tool (WinRAR, 7Zip, etc). The extracted contents will include the “Payload.bin” file, which is what you’d need to extract. Copy the Payload.bin file inside the “payload_dumper” folder.

#### 3. Open the command-line window on your PC in the ‘payload_dumper’ folder, where the tool and the payload.bin files are present.

#### 4. On Windows

```bash
python -m pip install protobuf
```
#### 5. On Windows

```bash
python payload_dumper.py payload.bin
```

### If error
- TypeError: Descriptors cannot not be created directly.
- Downgrade the protobuf package to 3.20.x or lower.
- Set PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python (but this will use pure-Python parsing and will be much slower).

```bash
pip install protobuf==3.20.*
```
