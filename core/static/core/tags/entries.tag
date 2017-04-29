<entries>
    <p class="mb-4 clearfix row-fix">
        <pager update={ getEntries }/>
    </p>

    <form onsubmit={ submitEntry }>
        <div class="row form-row mb-5 shadow-muted">
            <div class="col-sm-3">
                <select class="custom-select" ref="project" required>
                    <option value="" disabled selected>Project</option>
                    <option each={ projects } value={ url }>{ name }</option>
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
                       onkeyup={ timer }
                       ref="duration"
                       placeholder="0:00"
                       value="{ timerDuration }"
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


    <script>
        this.timerState = 'Start'


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
                    var interval = setInterval(this.tick, 1000, this)
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
            let projects = quickFetch(projectsApiUrl)

            Promise.all([entries, projects]).then(function(e) {
                let dates = []
                $.each(e[0].results, function(i, entry) {
                    if ($.inArray(entry.date, dates) === -1) {
                        dates.push(entry.date)
                    }
                })

                this.update({
                    dates: dates,
                    entries: e[0].results,
                    projects: e[1].results,
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
            this.getEntries()
        }.bind(this))
    </script>
</entries>
