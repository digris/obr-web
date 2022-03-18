import { describe, it, expect } from 'vitest'

import { mount } from '@vue/test-utils'
import ColorChoser from '@/components/colors/ColorChooser.vue'

describe('ColorChoser', () => {
  it('renders properly', () => {
    const wrapper = mount(ColorChoser, { props: { msg: 'Hello Vitest' } })
    expect(wrapper.text()).toContain('')
  })
})
