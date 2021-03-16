python-rest-sample
=========

![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)
![Mysql 3.9](https://img.shields.io/badge/mysql-8-blue.svg)

python-rest-sample is a boilerplate example project illustration how one could go about implementing a RESTful API
using **Python**, **Flask** and **SQLAlchemy**.

## Functionality

* [x] Implemented CRUD endpoints for Profiles and Interactions - with relations
* [x] Responses with pagination, sorting and filtering
* [x] Integrated with Database, MySQL
* [x] Input validation and exception handling
* [x] Geo Address lookup and coordinates methods (not applied)
* [x] Unit test for models
* [x] Functional test via Postman
* [x] User guide with data and code samples

#### Todo

* [ ] Interactive "/environment/build/docker.sh" script to push/pull image to/from docker registry for environment versioning
* [ ] Ability to detect and execute new database migration scripts
* [ ] Add friendly description to documentation along with required fields and lengths
* [ ] Add additional negative tests for error and validation handling

## Resources

- Postman Collection for testing, https://raw.githubusercontent.com/ppetroski/python-rest-sample/master/resources/sample.postman_collection.json
- HTML User Guide (generated from postman collection and homegrown tool), https://htmlpreview.github.io/?https://github.com/ppetroski/python-rest-sample/blob/master/resources/guide.html

## Setup

#### Docker (Mac & Linux)

- git clone https://github.com/ppetroski/python-rest-sample.git
- Ensure ports 5000 and 3306 are free so the contains can bind them
- Run the docker script that builds the image, configures the containers and starts them

```
sh ./environment/build/docker.sh
```
- (Optional) Run unit tests
```
docker exec -it sample-app python -m pytest
```

Notes:

- Configuration changes for the virtual IP might be required
- ./environment/docker.sh can be run repeatedly but any database entries will be wiped. If the containers are not running
  use *docker restart sample-db* & *docker restart sample-app*

#### Manual (Bring Your Own MySQL)

- git clone https://github.com/ppetroski/python-rest-sample.git
- pip3 install -r requirements.txt
- Configure ./config.py with the appropriate database connection
- MySQL scripts are in migration for creating the bas schema

```
mysql sample -u web_user -p < ./environment/build/migrations/profile.sql
mysql sample -u web_user -p < ./environment/build/migrations/interaction.sql
```

- Launch the app using your IDE or the *python3.9 app.py*
- (Optional) Run unit tests
```
python3.9 -m pytest
```

## Creating an additional endpoint

Let's assume we need a new API to correlate interactions with to a campaign. To achieve this we will create a new object
and alter the existing interaction model.

Steps for introducing the new API endpoint

- Create an object data model (./models/campaign.py)

```python
import components.validator as validator
from components.framework.baseModel import BaseModel, RelationsBase
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, validates


class Campaign(BaseModel, RelationsBase):
  __tablename__ = 'evt_Campaign'
  _remove_columns = ['updated_at', 'deleted_at']
  # Model attributes
  trk_Interaction = Column(Integer, ForeignKey('trk_Interaction.id'))
  type = Column(String(length=50))
  name = Column(String(length=50))
  location = Column(String(length=50))
  # Model relationships
  interactions = relationship("Interaction", back_populates="campaign")

  @validates("type")
  def validate_type(self, key, value):
    value = value.upper()
    validator.has_value(self, key, value, ['IN-PERSON', 'EMAIL', 'PHONE', 'SMS'])
    return validator.is_string(self, key, value)

  @validates("name")
  def validate_outcome(self, key, value):
    return validator.is_string(self, key, value)

  @validates("location")
  def validate_outcome(self, key, value):
    return validator.is_string(self, key, value)
```

- Create Database migration script (./environment/build/migrations/campaign.sql)

```
DROP TABLE IF EXISTS `evt_Campaign`;
CREATE TABLE `evt_Campaign` (
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` timestamp NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  `uuid` varchar(50) NOT NULL UNIQUE,
  `type` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `location` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
```

- Add a controller to handle the requests (./controllers/campaign.py)

```python
from components.framework.baseController import BaseController
from models.campaign import Campaign


class Campaign(BaseController):
    # At this time all we need to do is define the model to enable CRUD endpoints for it
    _model = Campaign
 ```

- Add routes (./app.py)

```python
from controllers.campaign import Campaign
api.add_resource(Interaction, '/campaign', '/campaign/<uuid>')
 ```

Steps for modifying the interactions model

- Add a new field, relation and validation (./models/interaction.py)

```python
evt_Campaign = Column(Integer, ForeignKey('evt_Campaign.id'))

campaign = relationship("Campaign", back_populates="interactions")

@validates("evt_Campaign")
def validate_type(self, key, value):
    return validator.is_int(self, key, value)
```

- Create Database migration script (./environment/build/migration/interaction_campaign.sql)

```
ALTER TABLE trk_Interaction ADD evt_Campaign INT;
ALTER TABLE trk_Interaction ADD CONSTRAINT fk_campaign_id  FOREIGN KEY (evt_Campaign) REFERENCES evt_Campaign(id);
```

- Execute MySQL Migration scripts (Docker examples)

```
docker exec -i sample-db mysql sample -u web_user -pdev < ./environment/build/migrations/campaign.sql
docker exec -i sample-db mysql sample -u web_user -pdev < ./environment/build/migrations/interaction_campaign.sql
```

