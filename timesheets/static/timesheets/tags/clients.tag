<clients>
    <div class="mb-4 clearfix">
        <pager update={ getClients }/>
    </div>

    <div class="row py-1 bg-inverse text-white font-weight-bold">
        <div class="col-sm-6">
            Client
        </div>
        <div class="col-sm-2">
            Total Time
        </div>
        <div class="col-sm-2">
            # Related
        </div>
        <div class="col-sm-2">
        </div>
    </div>

    <form class="row mb-4 py-2 bg-faded" onsubmit={ submitClient } if={ perms && perms.add_client }>
        <div class="col-10">
            <input type="text"
                   class="form-control form-control-sm"
                   ref="name"
                   placeholder="New Client Name"
                   required>
        </div>
        <div class="col-2">
            <button type="submit" class="btn btn-success btn-sm w-100">
                Add
            </button>
        </div>
    </form>

    <client each={ clients } perms={ perms } />


    <script>
        getClients(url) {
            url = (typeof url !== 'undefined') ? url : clientsApiUrl;
            quickFetch(url).then(function(data) {
                this.update({
                    clients: data.results,
                    next: data.next,
                    previous: data.previous
                });
            }.bind(this));
        }


        submitClient(e) {
            e.preventDefault();
            let body = {
                name: this.refs.name.value
            };
            quickFetch(clientsApiUrl, 'post', body).then(function(data) {
                this.refs.name.value = '';
                if (data.id) {
                    this.clients.unshift(data);
                    this.update();
                }
            }.bind(this));
        }


        getPerms() {
            quickFetch('/api/permissions/').then(function(data) {
                   let perms = Object;
                   $.each(data.results, function(i, perm) {
                        perms[perm.codename] = perm;
                    });
                   this.perms = perms;
                });
        }

        this.on('mount', function() {
            this.getPerms();
            this.getClients();
        }.bind(this));
    </script>
</clients>
