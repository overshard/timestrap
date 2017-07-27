## Multiple Sites

Timestrap supports setting up multiple sites with configurations options 
available on a per-site basis. This functionality may be useful if, for 
example, there is a need to separate departments or functional teams within a 
larger group of organization.

Sites can be managed by any user with admin access and appropriate permissions:
either `superuser` or the various `site` and `conf` permissions. Sites are 
based on domain and use two primary settings, `domain` and `name` in addition 
to the various configuration options available.

### Data Sharing

All Timestrap data will be related to either one or multiple sites.

- **Clients** and **Tasks** can be related to *multiple* sites.
- **Entries** and **Invoices** can be related to a *single* site.

Data with a single-site relationship will automatically be related to the site 
it was entered on. This settings can be changed from the admin site.

Currently, multiple site relationships can only be controlled from the admin
site. To use a Client or Task on multiple sites, it must be added to one 
site and then modified in the admin site to be related to additional sites.
