# A simple script to do some load test for camunda

## Usage

### Deploy a Process

- Go to camunda_host:port/manager
- Login with tomcat admin user/pwd
- Select WAR file to upload
- Deploy

### Get Process ID

- Go to camunda_host:port/camunda/app
- Click "Processes" from the top menu bar
- Click the name of the process you just deployed/want to test
- Copy Definition ID

### Config Load Test Tool

Set configurations in "config.ini"

TotalRequestsToSend: total requests per thread to send. Set to -1 if you want to loop infinitely.

CamundaHost: http://camunda_host:camunda_port.

ProcessID: the id of the process you want to test.

By default there will be 50 processes running at the same time. If you want to change that, update in "start_load_test" shell script.

### Start Load Test
Copy "camunda_log_clean" scripts to camunda logs directory and run.

This script will clean catalina.out and localhost_access log of the current date, so that analysis based on the log is easier.

Then start the load test by running: `./start_load_test`

### Collecting Results

#### Client Side

Each thread will generate a "\*.log" file which contains a simple static, showing how many requests are sent, and how many returns HTTP 200, etc.

#### Camunda Server Side Log Analysis

Calculating how many requests camunda handles per second is easier based on camunda log files.

To do so:

Copy "camunda_log_statics" to camunda server logs directory and run it.

This will give you a static based on camunda access log, showing how many requests in all, how many are OK, how many are HTTP 500, and how many requests are processed per second. 
