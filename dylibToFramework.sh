#!/bin/bash

# This script converts .dylib files into iOS AppStore compatible .frameworks
# and also takes care of already present .frameworks

path_to_search=$1
path_to_qtMetadataExtractor=$2

if [ "$path_to_search" != "" ]; then

echo "*** dylibToFramework.sh starting ***"

declare -a dylibs

# Search for dylibs
while IFS=  read -r -d $'\0'; do
    dylibs+=("$REPLY")
done < <(find $path_to_search -name "*.dylib" -type f -print0)

for dylib in "${dylibs[@]}"; do
  echo "Processing dynamic library: $dylib"

  lib_basename=$(basename "$dylib" .dylib)
  lib_basename=$(echo $lib_basename | sed "s/\.[0-9].*//")
  lib_bundlename=$(echo $lib_basename | sed "s/[^a-zA-Z]//g")
  lib_directory=$(dirname "$dylib")
  framework="$lib_directory/$lib_basename.framework"

  echo "Creating framework: $framework"

  # Create a framework folder and copy the library into it
  mkdir -p "$framework"
  new_dylib="$framework/$lib_basename"
  cp "$dylib" "$new_dylib"

  # Some libraries seem to be already signed, remove this
  codesign --remove-signature "$new_dylib"

  #clean_basename=$(echo "$lib_basename._ /" | tr -cd '[a-zA-Z0-9]')
  bundle_indentifier="com.company.$lib_bundlename"
  min_os_version="11.0"

  # Create a plist file for each dylib
  echo "Creating Info.plist..."
cat >"$framework/Info.plist" <<EOL
  <?xml version="1.0" encoding="UTF-8"?>
  <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
  <plist version="1.0">
  <dict>
    <key>CFBundleExecutable</key>
    <string>${lib_basename}</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleIdentifier</key>
    <string>${bundle_indentifier}</string>
    <key>CFBundlePackageType</key>
    <string>FMWK</string>
    <key>CFBundleShortVersionString</key>
    <string>4.0</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>CFBundleVersion</key>
    <string>4.0</string>
    <key>MinimumOSVersion</key>
    <string>${min_os_version}</string>
  </dict>
  </plist>
EOL

  cat "$framework/Info.plist"

  # Extract Qt metadata to separate json file if it is a Qt dylib plugin
  if [ -f "$path_to_qtMetadataExtractor" ]; then
    echo "Extracting QtMetadata..."
    "$path_to_qtMetadataExtractor" -o "$framework/$lib_basename.json" "$new_dylib"
  fi

done

declare -a frameworks
declare -a new_dylibs
while IFS=  read -r -d $'\0'; do
    framework_find_result=("$REPLY")
    frameworks+=$framework_find_result
    framework_basename=$(basename "$framework_find_result" .framework)
    new_dylibs+=( $(echo "$framework_find_result/$framework_basename") )
done < <(find $path_to_search -name "*.framework" -type d -print0)

# Change all library name dependencies
echo "Changing library name dependencies..."
for dylib_outer in "${new_dylibs[@]}"; do
  basename_outer=$(basename "$dylib_outer")
  library_id=$(otool -DX "$dylib_outer")
  install_name_tool -id "@rpath/$basename_outer.framework/$basename_outer" "$dylib_outer"

  for dylib_inner in "${new_dylibs[@]}"; do
    install_name_tool -change "$library_id" "@rpath/$basename_outer.framework/$basename_outer" "$dylib_inner"
  done
done

# The MinimumOSVersion key has to be present in each framework
echo "Checking the Info.plist file in all frameworks..."
for framework in "${frameworks[@]}"; do
  plist_file="$framework/Info.plist"
  echo "Checking $plist_file for the right MinimumOSVersion entry..."
  if [ -f "$plist_file" ]; then
    if grep -Fq "<key>MinimumOSVersion</key>" "$plist_file"; then
      echo "Replacing..."
      plutil -replace MinimumOSVersion -string "${min_os_version}" "$plist_file"
    else
      echo "Adding..."
      plutil -insert MinimumOSVersion -string "${min_os_version}" "$plist_file"
    fi
  fi
done

echo "*** dylibToFramework.sh finished ***"

fi
