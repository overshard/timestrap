# Sites

Timestrap takes advantage of [Django's "sites" framework](https://docs.djangoproject.com/en/1.11/ref/contrib/sites/)
to support running multiple Timestrap "sites" from a single instance of the
application. This an optional enhancement, and the base Timestrap application
will work fine as a single site without any advanced configuration.

## Single Site

Out of the box, Timestrap is a single site using the fake domain `time.strap`
and name `Timestrap`. Both the name and the domain name are configurable on
the admin.

Any domain will fall back to the default site, but it is recommended to at
least set the site domain setting be updated to match the actual site domain
since emails will use this domain when sending.

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
- **Entries** can be related to a *single* site.

Data with a single-site relationship will automatically be related to the site
it was entered on. This settings can be changed from the admin site.

Currently, multiple site relationships can only be controlled from the admin
site. To use a Client or Task on multiple sites, it must be added to one
site and then modified in the admin site to be related to additional sites.

### Example: Big Project Builders, Inc.

Big Project Builders, Inc. (BPB) uses Timestrap to keep track of its progress
for various projects & clients. However, with many different teams a single
Timestrap instance would have *a lot* of data and it may come difficulty for
individual employees to keep track of progress. So BPB decides to break the
instance in to multiple sites -

- **timestrap.bpb.io** is the primary instance site, where admin superusers add
the Clients and Projects that BPB is working on.
- **design.timestrap.bpb.io** is used by BPB's designers to assign and track
graphics and design work for projects.
- **development.timestrap.bpb.io** is used by BPB's developers to assign and
track project development.
- **testing.timestrap.bpb.io** is used bu BPB's testing team to record time
spent executing and reporting on project tests.
