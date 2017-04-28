<entries>
    <p class="mb-4 clearfix row-fix">
        <pager update="{ getEntries }"/>
    </p>


    <form onsubmit={ submitEntry }>
        <div class="row form-row mb-5 shadow-muted">
            <div class="col-sm-3">
                <select class="custom-select" ref="project">
                    <option value='' class="text-muted">Project</option>
                    <option each={ projects } value={ url }>{ name }</option>
                </select>
            </div>
            <div class="col-sm-5">
                <input type="text" class="form-control form-control-lg" ref="note" placeholder="Note">
            </div>
            <div class="col-sm-2">
                <input type="text" class="form-control form-control-lg" onkeyup={ timer } ref="duration" placeholder="0:00" value="{ timerDuration }">
            </div>
            <div class="col-sm-2">
                <button type="submit" class="btn btn-success btn-lg" onclick={ timer }>{ timerState }</button>
            </div>
        </div>
    </form>

    <div class="mb-5" each={ dates }>
        <h5 class="text-muted">{ mainDate }</h5>
        <div class="entries-rows shadow-muted row-fix">
            <entry each={ entries } if={ mainDate === date } id="entry-{ id }" class="row py-2" />
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

    <script>
        var interval
        this.timerState = 'Start'
        this.hours = 0
        this.minutes = 0
        this.seconds = 0



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
            // TODO: Cleanup
            if (duration && this.timerState !== 'Stop') {
                this.timerState == 'Start'
            } else {
                if (this.timerState === 'Start') {
                    this.timerState = 'Stop'
                    interval = setInterval(this.tick, 1000, this)
                    e.preventDefault()
                } else {
                    this.timerState = 'Add'
                    clearInterval(interval)
                    this.timerDuration = pad(this.hours) + ':' + pad(this.minutes)
                    this.hours = 0
                    this.minutes = 0
                    this.seconds = 0
                    e.preventDefault()
                }
            }
        }


        getEntries(url) {
            url = (typeof url !== 'undefined') ? url : entriesApiUrl

            let entries = quickFetch(url)
            let users = quickFetch(usersApiUrl)
            let projects = quickFetch(projectsApiUrl)

            Promise.all([entries, users, projects]).then(function(e) {
                let dates = []
                $.each(e[0].results, function(i, el) {
                    if ($.inArray(el.date, dates) === -1) {
                        dates.push(el.date)
                    }
                })
                // Doing this in another loop and not the previous because
                // inArray doesn't seem to match objects very well here.
                let dateObjects = []
                $.each(dates, function(i, el) {
                    dateObjects.push({mainDate: el})
                })

                this.update({
                    dates: dateObjects,
                    entries: e[0].results,
                    users: e[1].results,
                    projects: e[2].results,
                    totalTime: e[0].total_duration,
                    subtotalTime: e[0].subtotal_duration,
                    next: e[0].next,
                    previous: e[0].previous
                })
            }.bind(this))
        }


        submitEntry(e) {
            e.preventDefault()
            let body = {
                user: usersApiUrl + userId + '/',
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
            this.getEntries()
        }.bind(this))
    </script>
</entries>
