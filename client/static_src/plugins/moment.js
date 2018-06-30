import moment from 'moment';
import 'moment-timezone';
import momentDurationFormat from 'moment-duration-format';


const VueMoment = {
  install: Vue => {
    momentDurationFormat(moment);
    moment.locale(timestrapConfig.SITE.LOCALE);
    Vue.prototype.$moment = moment;
  },
};


export default VueMoment;
