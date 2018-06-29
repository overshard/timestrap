import moment from 'moment';
import 'moment-timezone';


const VueMoment = {
    install: Vue => {
        moment.locale(timestrapConfig.SITE.LOCALE);
        Vue.prototype.$moment = moment;
    }
};

export default VueMoment;
