# SimpleForensics

SimpleForencs is an app to do simple tasks of a forensic environment.

## Simple Imager
At the moment, only wipe and copy disks/files are implemented.

The syntax is same as `dd` to make you more confortable using it.

### Examples
**Warning**: Make sure to not change the values between `if=` and `of=`!

#### Forensic copies
 * Here a simple usage example of forensic copy
```
sudo ./SimpleImager.py if=/dev/sdb of=/media/images/img.dd
```
* Changing the buffer size to 1024 bytes
```
sudo ./SimpleImager.py if=/dev/sdb of=/media/images/img.dd bs=1024
```
* Copying the first 5 blocks with sizeof 1024 bytes
```
sudo ./SimpleImager.py if=/dev/sdb of=/media/images/img.dd bs=1024 count=5
```

#### Wipe
Here's a simple example of disk wipe
```
sudo ./SimpleImager.py of=/dev/sdb --wipe
```