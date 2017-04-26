<timesheets>
    <p class="mb-4 clearfix">
        <button class="btn btn-primary btn-sm"
                data-url="{ previous }"
                if={ previous }
                onclick={ timesheetsPage }>
            <i class="fa fa-arrow-left" aria-hidden="true"></i> Previous
        </button>

        <button class="btn btn-primary btn-sm pull-right"
                data-url="{ next }"
                if={ next }
                onclick={ timesheetsPage }>
            Next <i class="fa fa-arrow-right" aria-hidden="true"></i>
        </button>
    </p>

    <form onsubmit={ submitTimesheet }>
        <table class="timesheets-table table table-striped table-sm w-100 d-none">
            <thead class="thead-inverse">
                <tr>
                    <th>Name</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                <tr class="table-info">
                    <td>
                        <input type="text" class="form-control form-control-sm" ref="name" placeholder="Name">
                    </td>
                    <td class="text-right">
                        <button type="submit" class="btn btn-primary btn-sm">Add</button>
                    </td>
                </tr>
                <tr each={ timesheets } data-is="timesheet">
                </tr>
            </tbody>
        </table>
    </form>

    <p class="loading text-center my-5">
        <i class="fa fa-spinner" aria-hidden="true"></i>
    </p>

    <script>
        var self = this;


        getTimesheets(url) {
            url = (typeof url !== 'undefined') ? url : timesheetsApiUrl;
            $('.loading, .timesheets-table').toggleClass('d-none');
            quickFetch(url).then(function(data) {
                self.update({
                    timesheets: data.results,
                    next: data.next,
                    previous: data.previous
                });
                $('.loading, .timesheets-table').toggleClass('d-none');
            });
        }


        timesheetsPage(e) {
            self.getTimesheets(e.currentTarget.getAttribute('data-url'));
        }


        submitTimesheet(e) {
            e.preventDefault();
            let body = {
                name: self.refs.name.value
            }
            quickFetch(timesheetsApiUrl, 'post', body).then(function(data) {
                self.refs.name.value = '';
                self.timesheets.unshift(data);
                self.update();
            });
        }

        self.getTimesheets();
    </script>
</timesheets>
