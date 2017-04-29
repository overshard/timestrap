<entries>
    <p class="mb-4 clearfix row-fix">
        <pager update={ getEntries }/>
    </p>

    <form onsubmit={ submitEntry }>
        <div class="row form-row mb-5 shadow-muted">
            <div class="col-sm-3">
                <select class="custom-select" ref="project" required>
                    <option></option>  <!-- For select2 placeholder to work -->
                    <optgroup each={ c in clients } label={ c }>
                        <option each={ projects } value={ url } if={ c == client_details.name }>{ name }</option>
                    </optgroup>
                </select>
            </div>
            <div class="col-sm-5">
                <input type="text"
                       class="form-control form-control-lg"
                       ref="note"
                       placeholder="Note"/>
            </div>
            <div class="col-sm-2">
                <input type="text"
                       class="form-control form-control-lg"
                       oninput={ timer }
                       ref="duration"
                       placeholder="0:00"
                       value={ timerDuration }
                       required/>
            </div>
            <div class="col-sm-2">
                <button type="submit"
                        class="btn btn-success btn-lg"
                        onclick={ timer }>
                    { timerState }
                </button>
            </div>
        </div>
    </form>

    <div class="mb-5" each={ d in dates }>
        <h5 class="text-muted">{ d }</h5>
        <div class="entries-rows shadow-muted row-fix">
            <entry each={ entries }
                   if={ d === date }
                   class="row py-2"/>
        </div>
    </div>

    <div class="row bg-success text-white py-2 my-5">
        <div class="offset-sm-6 col-sm-2 text-right">
            Subtotal<br>
            <strong>Total</strong>
        </div>
        <div class="col-sm-2">
            { subtotalTime }<br>
            <strong>{ totalTime }</strong>
        </div>
    </div>


    <style>
    </style>


    <script>
        // TODO: There has to be a better way
        tick(entry) {
            if (entry.seconds === 60) {
                ++entry.minutes
                entry.seconds = -1
            }
            if (entry.minutes === 60) {
                ++entry.hours
                entry.minutes = 0
            }
            entry.update({
                hours: entry.hours,
                minutes: entry.minutes,
                seconds: ++entry.seconds,
                timerDuration: pad(entry.hours) + ':' + pad(entry.minutes) + ':' + pad(entry.seconds)
            });
        }


        timer(e) {
            let duration = this.refs.duration.value
            if (this.timerState === 'Start' && duration) {
                this.timerState = 'Add'
            } else if (this.timerState === 'Start') {
                this.timerState = 'Stop'
                this.timerDuration = '00:00:00'
                this.hours = 0
                this.minutes = 0
                this.seconds = 0
                interval = setInterval(this.tick, 1000, this)
                e.preventDefault()
            } else if (this.timerState === 'Stop') {
                clearInterval(interval)
                this.timerState = 'Add'
                this.timerDuration = pad(this.hours) + ':' + pad(this.minutes)
                this.hours = 0
                this.minutes = 0
                this.seconds = 0
                e.preventDefault()
            } else if (!duration) {
                this.timerState = 'Start'
                e.preventDefault()
            }
        }


        getEntries(url) {
            url = (typeof url !== 'undefined') ? url : entriesApiUrl

            let entries = quickFetch(url)
            let projects = quickFetch(projectsApiUrl)

            Promise.all([entries, projects]).then(function(e) {
                let dates = []
                $.each(e[0].results, function(i, entry) {
                    if ($.inArray(entry.date, dates) === -1) {
                        dates.push(entry.date)
                    }
                })

                let clients = []
                $.each(e[1].results, function(i, project) {
                    if ($.inArray(project.client_details.name, clients) === -1) {
                        clients.push(project.client_details.name)
                    }
                })

                this.update({
                    dates: dates,
                    clients: clients,
                    entries: e[0].results,
                    projects: e[1].results,
                    totalTime: e[0].total_duration,
                    subtotalTime: e[0].subtotal_duration,
                    next: e[0].next,
                    previous: e[0].previous
                })

                $('.custom-select').select2({placeholder: 'Project'});
            }.bind(this))
        }


        submitEntry(e) {
            e.preventDefault()
            let body = {
                user: userApiUrl,
                duration: this.refs.duration.value,
                note: this.refs.note.value,
                project: this.refs.project.value
            }
            quickFetch(entriesApiUrl, 'post', body).then(function(data) {
                this.refs.duration.value = ''
                this.refs.note.value = ''
                this.entries.unshift(data)
                this.timerState = 'Start'
                this.update()
            }.bind(this))
        }


        this.on('mount', function() {
            this.timerState = 'Start'
            this.getEntries()
        }.bind(this))
    </script>
</entries>
