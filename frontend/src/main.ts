import Avatar from "primevue/avatar";
import Badge from "primevue/badge/Badge.vue";
import Button from "primevue/button";
import ButtonGroup from "primevue/buttongroup";
import Card from "primevue/card";
import Column from "primevue/column";
import DataTable from 'primevue/datatable';
import Dialog from "primevue/dialog";
import IconField from "primevue/iconfield";
import InputNumber from "primevue/inputnumber";
import InlineMessage from "primevue/inlinemessage";
import Image from "primevue/image";
import InputIcon from "primevue/inputicon";
import InputText from "primevue/inputtext";
import OverlayPanel from "primevue/overlaypanel";
import Paginator from "primevue/paginator";
import ProgressSpinner from "primevue/progressspinner";
import Sidebar from "primevue/sidebar";
import SelectButton from "primevue/selectbutton";
import Splitter from "primevue/splitter";
import SplitterPanel from "primevue/splitterpanel";
import Timeline from "primevue/timeline";
import Tooltip from 'primevue/tooltip';

import "primevue/resources/themes/aura-light-noir/theme.css";
import "@/../public/styles.min.css";
import "@/../public/fonts/inglobal/inglobal.css";
import "@/../public/root.styles.css";
import 'primeicons/primeicons.css'

import {app} from '@/appInstance';
import store from "@/store";
import router from "@/router";
import setupInterceptors from '@/services/api/setupInterceptors.ts';
import Ripple from "primevue/ripple";

setupInterceptors();

app.directive('ripple', Ripple);
app.directive('tooltip', Tooltip);
app.use(store);
app.use(router);

app.component("Avatar", Avatar);
app.component("Badge", Badge);
app.component("Button", Button);
app.component("ButtonGroup", ButtonGroup);
app.component("Card", Card);
app.component("Column", Column);
app.component("DataTable", DataTable);
app.component("Dialog", Dialog);
app.component("InputNumber", InputNumber);
app.component("IconField", IconField);
app.component("Image", Image);
app.component("InlineMessage", InlineMessage);
app.component("InputIcon", InputIcon);
app.component("InputText", InputText);
app.component("OverlayPanel", OverlayPanel);
app.component("Paginator", Paginator);
app.component("ProgressSpinner", ProgressSpinner);
app.component("SelectButton", SelectButton);
app.component("Sidebar", Sidebar);
app.component("Splitter", Splitter);
app.component("SplitterPanel", SplitterPanel);
app.component("Timeline", Timeline);

app.mount('#app');
