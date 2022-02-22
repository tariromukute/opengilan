  #!/bin/bash

  # Configure the headers
  echo 'Configuring headers...'
  cd /usr/src/$(uname -r)

  # Create a ./.config file by using the default
  # symbol values from either arch/$ARCH/defconfig
  # or arch/$ARCH/configs/${PLATFORM}_defconfig,
  # depending on the architecture.
  make defconfig

  # Create module symlinks
  echo 'CONFIG_BPF=y' >> .config
  echo 'CONFIG_BPF_SYSCALL=y' >> .config
  echo 'CONFIG_BPF_JIT=y' >> .config
  echo 'CONFIG_HAVE_EBPF_JIT=y' >> .config
  echo 'CONFIG_BPF_EVENTS=y' >> .config
  echo 'CONFIG_FTRACE_SYSCALLS=y' >> .config
  echo 'CONFIG_KALLSYMS_ALL=y' >> .config

  # prepare headers
  echo 'Preparing headers...'
  make prepare

  # move into the bcc tools directory
  cd /usr/share/bcc/tools

  # Start a bash session
  bash