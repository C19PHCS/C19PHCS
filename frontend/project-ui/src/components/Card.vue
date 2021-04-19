<template>
  <q-card
    :style="`min-width: ${width}px;`"
    class="no-border"
  >
    <q-card-section class="flex text-white bg-primary">
      <div class="text-h6">
        {{ title }}
      </div>
      <q-space />
      <q-btn
        flat
        size="sm"
        v-close-popup
        round
        icon="close"
      />
    </q-card-section>
    <q-form @submit="$emit('submit')">
      <div style="min-height: 100px;">
        <q-card-actions
          align="right"
        >
          <q-btn
            flat
            color="primary"
            v-close-popup
          />
          <div>
            <q-btn
              :label="saveTitle"
              color="primary"
              type="submit"
            />
          </div>
        </q-card-actions>
      </div>
    </q-form>
  </q-card>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
  name: 'Card',
  props: {
    title: {
      type: String
    },
    width: {
      type: Number
    }
  },
  computed: {
    saveTitle(): string {
      return 'Save'
    },
    cancelTitle(): string {
      return 'Cancel'
    }
  },
  components: {
  }
});
</script>