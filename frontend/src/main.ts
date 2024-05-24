import {createApp} from 'vue';
import {Router} from "vue-router";
import PrimeVue from 'primevue/config';
import ToastService from 'primevue/toastservice';
import Avatar from "primevue/avatar";
import Button from "primevue/button";
import Column from "primevue/column";
import DataTable from 'primevue/datatable';
import Dialog from "primevue/dialog";
import IconField from "primevue/iconfield";
import InlineMessage from "primevue/inlinemessage";
import Image from "primevue/image";
import InputIcon from "primevue/inputicon";
import InputText from "primevue/inputtext";
import OverlayPanel from "primevue/overlaypanel";
import ProgressSpinner from "primevue/progressspinner";
import Sidebar from "primevue/sidebar";
import SelectButton from "primevue/selectbutton";
import Splitter from "primevue/splitter";
import SplitterPanel from "primevue/splitterpanel";
import Tooltip from 'primevue/tooltip';

// import "primevue/resources/themes/tailwind-light/theme.css"; // свежий
// import "primevue/resources/themes/soho-light/theme.css"; // скругленный
// import "primevue/resources/themes/fluent-light/theme.css"; // строгий
import "primevue/resources/themes/aura-light-noir/theme.css";
// import "primevue/resources/themes/aura-dark-noir/theme.css";
import "@/../public/styles.min.css";
import "@/../public/fonts/inglobal/inglobal.css";
import "@/../public/root.styles.css";
import 'primeicons/primeicons.css'

import App from '@/App.vue';
import store from "@/store";
import setupInterceptors from '@/services/setupInterceptors';
import router from "@/router";

setupInterceptors(store);
const app = createApp(App);
app.use(PrimeVue, {ripple: true});
app.use(ToastService);
app.directive('tooltip', Tooltip);
app.use(store);
app.use(router);
app.config.globalProperties.$router = router as Router;

app.component("Avatar", Avatar);
app.component("Button", Button);
app.component("Column", Column);
app.component("DataTable", DataTable);
app.component("Dialog", Dialog);
app.component("IconField", IconField);
app.component("Image", Image);
app.component("InlineMessage", InlineMessage);
app.component("InputIcon", InputIcon);
app.component("InputText", InputText);
app.component("OverlayPanel", OverlayPanel);
app.component("ProgressSpinner", ProgressSpinner);
app.component("SelectButton", SelectButton);
app.component("Sidebar", Sidebar);
app.component("Splitter", Splitter);
app.component("SplitterPanel", SplitterPanel);

app.mount('#app');
