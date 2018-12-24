nethserver-phpvirtualbox-5.2
============================

A rpm to configure phpvirtualbox 5.2 for NethServer

nethserver-phpvirtualbox-X.X has for dependencies nethserver-virtualbox-X.X (rpm to install VirtualBox) and phpvirtualbox. 
The versions are bind:

    nethserver-phpvirtualbox-5.2 requires phpvirtualbox-5.2 and nethserver-virtualbox-5.2
    nethserver-virtualbox-5.2 which requires VirtualBox-5.2

VirtualBox compile its modules with the last kernel, you must have the most updated kernel and to start on it at boot.

If the installer cannot compile the modules, then you should reboot your server and launch again the compilation by : ```/sbin/vboxconfig```

### Install the virtualbox repository

you could install the rpm nethserver-virtualbox-repository:

    yum install nethserver-virtualbox-repository

The virtualbox repository setting is bundled with the rpm nethserver-phpvirtualbox-X.X

### Oracle VM VirtualBox Extension Pack

This pack provides some good features like the usb support, Virtualbox RDP, disk encryption, NVMe and PXE boot for Intel cards. 
It is installed by the event nethserver-virtualbox-X.X-update automatically (by the installation or a rpm update). 
The pack is relevant of the VirtualBox version, if you need to update it, then trigger the event nethserver-virtualbox-X.X-update :

    signal-event nethserver-virtualbox-5.2-update

### phpvirtualbox configuration

These are the esmith properties to modify the settings of phpvirtualbox

    AdminGroup=vboxadmin       # members of this group can authenticate in  `AD` as administrators
    AdminUser=admin            # User list (comma separated) of administrators that can authenticate in `LDAP`
    AdvancedSettings=false     # Display the advanced settings in phpvirtualbox (true, false)
    Authentication=internal    # Authentication in phpvirtualbox: internal (builtin), AD (SAMBA AD), LDAP (openldap)
    DomainName=                # If set, a domain name or FQDN is used instead of https://server/phpvirtualbox
    QuotaPerUser=5             # Number maximal of VMs allowed for non admin user 
    TCPPortsRDP=9000-9100      # RDP ports for the console RDP of phpvirtualbox (the firewall is opened)
    URL=                       # If set, the path is modified to https://server/URL
    UserGroup=vboxuser         # members of this group can authenticate in  `AD` as simple users
    VMOwnerShip=true           # If set to true, users can see only their VM (true, false)
    access=private             # Restric phpvirtualbox access (private, public)
    accessRDP=green            # Access usage of the integrated RDP console (green, red)
    ipaddrRDP=                 # Set the IP of the integrated RDP console for specific need
    status=enabled             # Enable phpvirtualbox (disabled, enabled)

for example:

    config setprop phpvirtualbox accessRDP red AdvancedSettings enabled
    signal-event nethserver-phpvirtualbox-5.2-update

### vboxweb: the user of virtualbox

The user who runs virtualbox is ```vboxweb```, a home is created (/home/vboxweb) to store all the virtual machines (in VirtualBox VMs) 
and also the needed ISOs for creating your VM. The password of this user is stored in ```/var/lib/nethserver/secrets/virtualbox```.

You could open a session by ssh to download directly the ISO with wget, or push them by rsync or scp, directly from your computer. 
You could provide to the vboxweb user a ssh key and open a ssh session without password.

    rsync -avz XXXXXXX.iso vboxweb@IpOfServer:/home/vboxweb/
    scp XXXXXXX.iso vboxweb@IpOfServer:/home/vboxweb/

### Authentication in phpvirtualbox

#### Access Levels

phpVirtualBox essentially has two access levels. Admin users and non-admin users.
Admin users have access to the Users section of phpVirtualBox and can add, edit, remove other users (only for the `internal` method). 
They can also perform actions that change VM group memberships and manipulate VM groups (Rename, Group, Ungroup). 
Admins are also not limited on the virtual machine quota and can manage VM of other users. The VMs are visible only by the owner, as long as the property `VMOwnerShip` is to true.

You can change the authentication method by the property `Authentication` (internal, LDAP, AD)

#### internal

The default credentials are username: `admin` password: `admin`

Once logged in, you should change the default password through File -> Change Password.

In the phpvirtualbox user menu, you can create users, and set their permissions (only for the `internal` method)

#### LDAP (openldap)

This authentication method is simple, all users from Openldap can login, but only users in the property `AdminUser` are administrators (comma separated list)

#### AD (active directory)

This authentication method is better implemented, group based (you have to create manually the two groups): 

  * members of `vboxadmin` are administrators
  * members of `vboxuser` are non privilegied users

Members who are not belong of these two groups cannot use the phpvirtualbox web application. You can change the group name with the properties `UserGroup` and `AdminGroup`

### Documentation

The documentation is available at : https://github.com/phpvirtualbox/phpvirtualbox/wiki
