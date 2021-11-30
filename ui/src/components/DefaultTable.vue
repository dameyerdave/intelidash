<script setup>
  import { ref } from 'vue'
  import { capitalize, generalValueFormatter, actionFormatter, generalFilter } from '../utils'
  import { Edit16Filled, Delete16Filled } from '@vicons/fluent'
  import RowEditDialog from './RowEditDialog.vue'
  import http from '../utils/http'

  const props = defineProps({
    url: {
      type: String,
      required: true
    }
  })

  const columns = ref(null)
  const rows = ref(null)
  let metadata = ref(null)
  const bump = ref(0)

  const defaultActions = ['edit', 'delete']

  async function getData() {
    try{
      const resp = await http.get(`${props.url}meta/`)
      if (resp.status === 200) {
        metadata.value = resp.data
      } else {
        console.error(resp.status, resp)
      }
    } catch (err) {
      console.error(err)
    }
    const cols = {...metadata.value}
    // We avoid displaying the url column
    delete cols.url
    columns.value = Object.values(cols).map(c => {return { 
        field: c.field, 
        label: c.label, 
        type: c.type,
        filterOptions: {
          enabled: true, // enable filter for this column
          placeholder: capitalize(c.field), // placeholder for filter input
          filterFn: (data, filterString) => generalFilter(data, filterString, metadata.value[c.field])
        },
        formatFn: value => generalValueFormatter(value, metadata.value[c.field]),
      } 
    })
    columns.value.push({
      field: 'actions',
      label: 'Actions', 
      formatFn: actionFormatter,
    })
    console.log('columns', columns.value)
    try {
      const resp = await http.get(`${props.url}`)
      if (resp.status === 200) {
        const rws = resp.data
        rows.value = rws.map(r => {
          return {...r, actions: defaultActions}
        })
        console.log('rows', rows.value)
      } else {
        console.error(resp.status, resp)
      }
    } catch (err) {
      console.error(err)
    }
  }
  getData()

  // Edit dialog
  const editingRow = ref(null)
  const showEditDialog = ref(false)

  function __type_default(type) {
    if (type === 'string') {
      return ''
    }
    if (type === 'integer') {
      return -1
    }
    return null
  }

  function doAction(action, row = null) {
    console.log('doAction', action)
    if (action === 'edit') {
      editingRow.value = {...row}
      showEditDialog.value = true
    } else if (action === 'delete') {
      deleteRow(row)
    } else if (action === 'add') {
      const emptyRow = {}
      for (const column of columns.value) {
        emptyRow[column.field] = __type_default(column.type)
      }
      editingRow.value = emptyRow
      showEditDialog.value = true
    }
  }

  async function saveRow(row) {
    // Send the changes to the server
    try {
      if (row.id === -1) {
        const resp = await http.post(`${props.url}`, row)
        if (resp.status === 201) {
          // Add row to the table data
          const data = resp.data
          rows.value.unshift( {...data, actions: defaultActions} )
          refreshTable()
        }
      } else {
        const resp = await http.put(`${props.url}${row.id}/`, row)
        if (resp.status === 200) {
          // Apply the changes to the table data
          const data = resp.data
          const rowIdx = rows.value.findIndex(r => r.id === data.id)
          rows.value[rowIdx] = {...data, actions: defaultActions}
        }
      }
      
    }
    catch(error) {
      console.error(error)
    }
  }

  async function deleteRow(row) {
    // Send the changes to the server
    try{
      const resp = await http.delete(`${props.url}${row.id}/`)
      if (resp.status === 204) {
        // Delete the row from the table data
        const rowIdx = rows.value.findIndex(r => r.id === row.id)
        rows.value.splice(rowIdx, 1)
      }
    }
    catch(error) {
      console.error(error)
    }
  }

  function refreshTable() {
    console.log('refresh', bump.value)
    bump.value++
  }
</script>

<template>
  <div class="container">
    <div class="buttonbar">
      <n-space :wrap="false">
        <n-button type="success" @click="doAction('add')">Add</n-button>
      </n-space>
    </div>
    <vue-good-table
        v-if="columns && rows"
        :columns="columns"
        :rows="rows"
        :line-numbers="false" 
        compactMode 
        :sort-options="{
          enabled: true,
          multipleColumns: true,
          initialSortBy: {field: 'id', type: 'desc'}
        }"
        :search-options="{
          enabled: true,
          // trigger: 'enter',
          skipDiacritics: false,
          placeholder: 'Search...'
        }" 
        :pagination-options="{
          enabled: true,
          mode: 'records',
          perPage: 10,
          position: 'bottom',
          perPageDropdown: [10, 20, 50, 100],
          dropdownAllowAll: true,
          setCurrentPage: 1,
          nextLabel: 'next',
          prevLabel: 'prev',
          rowsPerPageLabel: '#/page',
          ofLabel: 'of',
          allLabel: 'All'
        }"
        :key="bump">
        <template #table-row="props">
          <!--<span v-if="props.column.field == 'content'">
          {{ props.row }}
          </span>-->
          <span v-if="props.column.field == 'actions'">
            <n-space :wrap="false">
              <template v-for="action in props.row.actions" :key="action">
                <n-button v-if="action === 'edit'" size="small" @click="doAction(action, props.row)">
                  <template #icon>
                    <n-icon color="#0e7a0d">
                      <edit-16-filled />
                    </n-icon>
                  </template>
                </n-button>
                <n-popconfirm 
                  v-if="action === 'delete'" 
                  positive-text="Yes" 
                  negative-text="No"
                  @positive-click="doAction(action, props.row)">
                  <template #icon>
                    <n-icon color="#ff0e0e">
                      <delete-16-filled />
                    </n-icon>
                  </template>
                  <template #trigger>
                    <n-button size="small">
                      <template #icon>
                        <n-icon color="#ff0e0e">
                          <delete-16-filled />
                        </n-icon>
                      </template>
                    </n-button>
                  </template>
                  Delete?
                </n-popconfirm>
              </template>
            </n-space>
          </span>
          <span v-else>
            {{props.formattedRow[props.column.field]}}
          </span>
        </template>
      </vue-good-table>
    </div>
    <RowEditDialog :metadata="metadata" :data="editingRow" :show="showEditDialog" @close="showEditDialog=false" @save="saveRow"/>
</template>

<style scoped>
.container {
  margin-left: 8px;
  margin-right: 8px;
}
.buttonbar {
  margin-bottom: 8px;
}
</style>