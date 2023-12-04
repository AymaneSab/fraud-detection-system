# Hive Installation on Ubuntu

## Download and Untar Hive

```bash
# Download Hive
wget https://downloads.apache.org/hive/hive-3.1.2/apache-hive-3.1.2-bin.tar.gz

# Untar Hive
tar xzf apache-hive-3.1.2-bin.tar.gz
```
## Configure Hive Environment Variables
### Update .bashrc

```
# Edit .bashrc
sudo gedit ~/.bashrc

# Add the following lines at the end of the file
export HIVE_HOME=/usr/local/Hive/apache-hive-3.1.2-bin
export PATH=$PATH:$HIVE_HOME/bin

# Save and close the file

# Source the updated .bashrc
source ~/.bashrc
```

## Edit hive-config.sh
```
# Edit hive-config.sh
sudo nano $HIVE_HOME/bin/hive-config.sh

# Add the following line
export HADOOP_HOME=/path/to/your/hadoop
# Save and close the file
```

## Create Hive Directories in HDFS

```
# Create tmp Directory
hdfs dfs -mkdir /tmp

# Add write and execute permissions to tmp group members
hdfs dfs -chmod g+w /tmp

# Create warehouse Directory
hdfs dfs -mkdir -p /user/hive/warehouse

# Add write and execute permissions to tmp group members
hdfs dfs -chmod g+w /user/hive/warehouse
```

## Configure hive-site.xml File (Optional)

```
# Navigate to the Hive conf directory
cd $HIVE_HOME/conf

# Copy the template to create hive-site.xml
cp hive-default.xml.template hive-site.xml

# Edit hive-site.xml
sudo gedit hive-site.xml
# Add any additional configurations if needed
```

## Initiate Derby Database

```
# Run the following command to initiate Derby database
$HIVE_HOME/bin/schematool -dbType derby -initSchema
```

## Launch Hive

```
# Navigate to Hive bin directory
cd $HIVE_HOME/bin

# Start Hive
hive
```

