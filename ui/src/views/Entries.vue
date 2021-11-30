<script>
  import DefautlTable from '../components/DefaultTable.vue'

  export default {
    components: {
      DefautlTable   
    }
  }
</script>

<template>
  <h1>Entries {{ $route.params.id }}</h1>
  <DefautlTable url="/api/entries/" />
</template>

<style>

</style>