---
layout: post
author: "Colin Stevens"
date: 2014-07-14 10:34 PM
author_mail: "&#109;&#097;&#105;&#108;&#064;&#099;&#111;&#108;&#105;&#110;&#106;&#115;&#116;&#101;&#118;&#101;&#110;&#115;.&#099;&#111;&#109;"
title:  "Creating a LUKS Encrypted Disk from Scratch"
tags: ["encryption", "LUKS"]
---
You want to encrypt an entire disk with [LUKS](https://en.wikipedia.org/wiki/Linux_Unified_Key_Setup) and don't know how? Good, read on.

# Step 1: Backup Your Data
This should seem obvious but for good measure I'll make sure to mention it. The process of converting a drive to an encrypted drive will destroy all data on it, so back up all. data you want to save to another disk and move it back at the end of the tutorial.

# Step 2: Partition the Disk
For partitioning the disk, we'll be using [fdisk](https://linux.die.net/man/8/fdisk):
{% highlight shell-session %}
$ fdisk /dev/sdX
{% endhighlight %}
Where X is the device identifier of the drive you're encrypting. Once you're in fdisk, type **o** to clear out any existing partition table, **n** for a new partition, **p** for a primary partition, press **ENTER** to accept the default partition number (1), **ENTER** again to accept the default starting sector, and **ENTER** a third time to accept the default ending sector (the end of the disk). It should then say something like this:
{% highlight shell-session %}
Created a new partition 1 of type 'Linux' and of size 1.8 TiB.
{% endhighlight %}
If it's not created as type Linux, press **t** to specify its type, then **83** to select Linux.
Finally, press **w** to write the partition table, then use fdisk to verify:
{% highlight shell-session %}
$ fdisk -l /dev/sdX
{% endhighlight %}
You should see something like this:
{% highlight shell-session %}
Device     Boot Start        End    Sectors  Size Id Type
/dev/sdX1        2048 3906963455 3906961408  1.8T 83 Linux
{% endhighlight %}

# Step 3: Generating a Keyfile
Next we'll create a keyfile for LUKS to use so we can automount it. We'll do this again with [dd](http://man7.org/linux/man-pages/man1/dd.1.html):
{% highlight shell-session %}
$ dd if=/dev/urandom of=/root/luks.key bs=4K count=1
{% endhighlight %}
This will create a 4KB keyfile of random data. Next it's smarter to change its permissions to avoid it being read by non-root users:
{% highlight shell-session %}
$ chmod 600 /root/luks.key
{% endhighlight %}
**KEEP THIS KEYFILE SAFE.** It functions just like a password, so don't keep it anywhere insecure or lose it. Instead of luks.key, a smarter name might be to use the drive's [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier). This way it's harder to confuse it with any other keyfiles you may have on your machine. To get the drive's UUID:
{% highlight shell-session %}
UUID="f9a0918c-59f0-46ca-edb4-aa2618348429" TYPE="crypto_LUKS" PARTUUID="3107d84d-01"
{% endhighlight %}
Then rename your luks.key keyfile with [mv](https://linux.die.net/man/1/mv):
{% highlight shell-session %}
$ mv /root/luks.key /root/UUID.key
{% endhighlight %}
Where UUID is the UUID found from blkid

# Step 4: Adding the LUKS Header
Finally onto actually putting LUKS on the drive. This is done with [cryptsetup](https://linux.die.net/man/8/cryptsetup): 
{% highlight shell-session %}
$ cryptsetup --cipher aes-xts-plain64 --key-size 512 --hash sha512 --iter-time 5000 luksFormat /dev/sdX1 /root/KEYNAME.key
{% endhighlight %}
Again where X is the drive identifier of the disk you'll be writing the header to, and KEYNAME.key is the name of your keyfile.

Optionally, you can add an additional key to the header. This can be a different keyfile or a password. Having a password in one of the keyslots can be helpful if you misplace your keyfile or are trying to decrypt the volume without it. To add a password to the header:
{% highlight shell-session %}
$ cryptsetup luksAddKey /dev/sdX1 --key-file=/root/KEYNAME.key
{% endhighlight %}
keeping in mind to change KEYNAME.key to your appropriate keyfile.
cryptsetup will then ask you to enter a new password and, once it's finished, you can verify that the key has been added by dumping the header information:
{% highlight shell-session %}
$ cryptsetup luksDump /dev/sdX1
{% endhighlight %}
You should see two keyslots enabled

# Step 5: Opening the LUKS Volume and Zeroing the Drive
The next step is to destroy all existing data on the drive, which can be done by writing zeros to every bit on the disk. This is important because LUKS won't fill your drive with nonsense data immediately after creation. Instead, it creates the LUKS header on the drive and subsequent data writes will be encrypted and written as nonsense. As such, you need to destroy all existing data on the drive as it would remain unencrypted until it happened to be overwritten with standard LUKS encrypted data.

This step provides additional security by hiding the write patterns and the occupied encrypted space on the drive, the latter of which can then lead to someone figuring out roughly how many files are encrypted on the device due to ext's predictable nature.

Zeroing the drive can be done fairly easily with [dd](https://linux.die.net/man/1/dd). But before doing this, we need to mount the newly created LUKS volume. This is done through cryptsetup:
{% highlight shell-session %}
$ cryptsetup luksOpen /dev/sdX1 luksdrive --key-file=/root/KEYNAME.key
{% endhighlight %}
and then use dd:
{% highlight shell-session %}
$ dd if=/dev/zero of=/dev/mapper/luksdrive bs=4M
{% endhighlight %}

**Make double sure you're zeroing the correct drive.** The last thing you want to do is destroy the data on the wrong disk. Also note that this process will probably take a very long time. For reference it took me roughly 13 hours to zero out a 2TB disk.

# Step 6: Create the File System and Set Up Auto-mounting
Now we need to write a filesystem to the space so it's useful. Write the filesystem with [mkfs](https://linux.die.net/man/8/mkfs.ext4):
{% highlight shell-session %}
$ mkfs.ext4 /dev/mapper/luksdrive
{% endhighlight %}
And you're finished. To make the drive automount at boot, add entries to [/etc/crypttab](https://linux.die.net/man/5/crypttab) and [/etc/fstab](https://linux.die.net/man/5/fstab) according to the following scheme:
{% highlight shell-session %}
/etc/crypttab:
luksdrive UUID=f9a0918c-59f0-46ca-edb4-aa2618348429 /root/KEYNAME.key luks,timeout=360
/etc/fstab:
/dev/mapper/luksdrive /mnt ext4 defaults,errors=remount-ro 0 2
{% endhighlight %}
Also important to note is how to properly remove the device. Instead of just unplugging it, make you sure unmount it if it's been mounted:
{% highlight shell-session %}
$ umount /MOUNT/POINT
{% endhighlight %}
and then close the volume with cryptsetup:
{% highlight shell-session %}
$ cryptsetup close /dev/mapper/DRIVETITLE
{% endhighlight %}
And then remove the device.
