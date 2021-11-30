export function capitalize (string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

export function generalValueFormatter (value, metadata) {
  if (!value) return '-'
  if (metadata.type === 'field') {
    return metadata.choices.filter(c => c.value === value)[0].label
  }
  return value
}

export function generalFilter (data, filterString, metadata) {
  if (!data) return false
  if (metadata.type === 'string') {
    return data.toLowerCase().includes(filterString.toLowerCase())
  }
  if (metadata.type === 'field') {
    return metadata.choices.map(c => c.label).join(' ').toLowerCase().includes(filterString.toLowerCase())
  }
  return false
}

export function actionFormatter (actions) {
  return actions
}