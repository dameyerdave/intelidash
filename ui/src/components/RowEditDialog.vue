<script setup>
  import { ref, toRef, watchEffect } from 'vue'
  import { capitalize } from '../utils'

  const props = defineProps({
    show: {
      type: Boolean,
      required: true
    },
    metadata: {
      validator: value => value === null || typeof value === 'object', 
      required: true,
    },
    data: {
      validator: value => value === null || typeof value === 'object',
      required: true
    }
  })

  const emit = defineEmits([
    'close',
    'save'
  ])

  const show = ref('props.show')
  const data = ref('props.data')

  watchEffect(() => show.value = props.show)
  watchEffect(() => data.value = props.data)

  function close(_show) {
    if (!_show) {
      show.value = false
      emit('close')
    }
  }

  function save() {
    close(false)
    emit('save', data.value)
  }
  function cancel() {
    close(false)
  }
</script>

<template>
  <n-modal v-model:show="show" preset="dialog" title="Edit" :show-icon="false" @update:show="close">
    <n-form :model="data" ref="formRef">
      <template v-for="(value, key) in data" :key="key">
        <template v-if="key in props.metadata && key !== 'id'">
          <n-form-item :path="key" :label="capitalize(key)">  
            <n-input v-if="props.metadata[key].type === 'string'" v-model:value="data[key]" placeholder="..." />
            <n-input v-if="props.metadata[key].type === 'integer'" type="number" v-model:value="data[key]" placeholder="..." />
            <n-select v-if="props.metadata[key].type === 'field'" type="number" v-model:value="data[key]" :options="'choices' in props.metadata[key] ? props.metadata[key].choices : []" />
          </n-form-item>
        </template>
      </template>
    </n-form>
    <template #action>
      <n-space>
        <n-button type="error" @click="cancel">Cancel</n-button>
        <n-button type="success" @click="save">Save</n-button>
      </n-space>
    </template>
  </n-modal>
</template>