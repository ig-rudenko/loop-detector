<template>
  <div>
    <div class="py-2 flex flex-row align-items-center">
      <Avatar class="mr-2 shadow-3" shape="circle" size="large" image="https://ui-avatars.com/api/?size=32&name=igor&font-size=0.33&background=random&rounded=true"/>
      <div class="flex flex-column">
        <span class="py-1">{{userFullName}}</span>
        <span class="px-2 py-1 border-round w-fit select-none shadow-3" :class="userLevelClasses">{{userLevel}}</span>
      </div>
    </div>
    <div class="p-2 flex flex-row align-items-center">
      <i class="pi pi-envelope mr-2"/><span>{{user.email}}</span>
    </div>
  </div>
</template>

<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {User} from "@/services/user.ts";


export default defineComponent({
  name: "UserDetail",
  props: {
    user: {required: true, type: Object as PropType<User>},
  },

  computed: {
    userFullName() {
      let fullName = this.user.firstName + " " + this.user.lastName;
      if (fullName.length > 1) {
        return fullName
      }
      return this.user.username
    },

    userLevel() {
      if (this.user.isSuperuser) return "superuser"
      if (this.user.isStaff) return "staff"
      return ""
    },

    userLevelClasses() {
      if (this.user.isSuperuser) return ["bg-purple-300", "text-white"]
      if (this.user.isStaff) return ["bg-indigo-300", "text-white"]
      return []
    }
  }
})
</script>

<style scoped>

</style>