And all the grain of sand came together to form a stone that stands the test of time. #TeamSandStone-7

<h2>Sandstone ETL Pipeline</h2>

<h3>Overview</h3>

This project takes the totesys database stored in OLTP format in AWS and converts it into an OLAP database within an AWS data warehouse. 

This is done using the standard ETL model. First, the totesys database is checked by an ingester lambda run every 10 minutes by Eventbridge Scheduler, and any new data is downloaded as a new file into an AWS s3 bucket. This download sends an event notification to trigger the process lambda, accesses the new file and reconfigures it into a series of star-schema tables. From there, the transformed files are sent into the processed data s3 bucket, which sends an event notification to the uploader lambda. This triggers the uploader to send the newly created files into the data warehouse.

This process is fully logged, with each lambda sending log files to a matching log group on Cloudwatch. A metric filter is attached to each of these log groups, and any errors cause an SNS notification noting the lambda and the type of error to be sent to the Sandstone group email address.

<h3>Installation</h3>

This project is designed to be run through Github. Testing and installation are fully automated using the test-and-deploy and terraform-deploy actions respectively. From this, the complete project should be created on AWS Lambda, and automatically download and process the data from the original database. 

These AWS processes are run entirely through Terraform code contained within the repo, including the lambdas, permissions, alarms, and layers. The dependencies for the custom-made layer are contained in the Python folder, while the processor and uploader lambdas also use the AWS Pandas managed layer. 

To clone the repo, you will need to set up your own secrets on Github, which should include the full access keys for the totesys database, a data warehouse on AWS to send data to, and the credentials for an AWS account to run the processing system on. You can see what names you’ll need to give these secrets under the deploy-terraform.yml file in .github. As part of copying this repo, you may also want to change the email address used for SNS notifications if you don’t have access to the currently configured one.
Because this is run entirely on the cloud, it’s unlikely that there should need to be multiple copies of this repo running at the same time. If there are, they should point to different data warehouses to avoid file duplication. 

<h3>Usage</h3>

This project should not require human input to run past its creation through Github. Once it has started running, all the user should need to do is access the files in the data warehouse. 

<h3>Technologies</h3>

Python: We used Python as it provides great resources to manage datasets in a safe and controlled manner.

PostgreSQL: This was used to collect and store data from a DataBase to a DataWarehouse.

Terraform: This was used to automate the creation of the required AWS resources.

AWS: Amazon Web Services was suitable as a basic and widely-used cloud computing service.

GitHub Actions: We built a CI/CD workflow to automate as much as possible and minimise the risk of human error.

TDD: We used Pytest to test our Python code and ensure there was a minimum coverage of 90%.

<h3>Methodologies</h3>

Agile: We had daily stand ups to ensure every member of the team knew what progress was made the day prior, what the plan was today and any issues that anyone was dealing with. This allowed for effective communication between the entire team.

Pair Programming: we used pair programming extensively to encourage collaboration, learn from each other and support each other.

Trello: we broke down every task into smaller granular tasks. Every time we completed one we would move the ticket to the appropriate section. This allowed us to know who was working on what, this greatly increased the efficiency of the team.

Slack: We communicated via slack throughout the project for stand ups and reaching out for advice.

<h3>Standards</h3>

Flake8: we used flake8 to ensure we met pep8 compliance to maintain clean, readable code.

<h3>The team</h3>

Andrea Olivier, aka andreaolivier
George Baldwin, aka GeorgeJB3
John Mustchin, aka Human0467
Sesan Olaiya, aka sesanolaiya
Pablo Bravo Galindo, aka pablobgldo
Ian Russell, aka ian512549

