<script setup lang="ts">
import { reactive, ref } from 'vue'
import { Clock, Mail, MapPin, Phone, Send } from 'lucide-vue-next'

import Button from '@/components/common/Button.vue'
import Card from '@/components/common/Card.vue'
import GhostTitle from '@/components/common/GhostTitle.vue'
import SectionTitle from '@/components/common/SectionTitle.vue'
import { useScrollAnimation } from '@/composables/useScrollAnimation'
import { usePortfolioStore } from '@/stores/portfolio'

const store = usePortfolioStore()
const { person } = store

const { target: formBlock } = useScrollAnimation<HTMLDivElement>()
const { target: infoBlock } = useScrollAnimation<HTMLDivElement>()

/* ---------- Форма ---------- */

const form = reactive({
  name: '',
  email: '',
  message: '',
})

const errors = reactive({
  name: '',
  email: '',
  message: '',
})

const isSent = ref(false)

const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

function validate(): boolean {
  errors.name = form.name.trim().length >= 2 ? '' : 'Введите имя (минимум 2 символа)'
  errors.email = emailPattern.test(form.email.trim()) ? '' : 'Введите корректный email'
  errors.message =
    form.message.trim().length >= 10 ? '' : 'Сообщение должно содержать минимум 10 символов'
  return !errors.name && !errors.email && !errors.message
}

function submitForm() {
  if (!validate()) return

  const subject = encodeURIComponent(`Заявка с сайта-визитки — ${form.name.trim()}`)
  const body = encodeURIComponent(
    `Имя: ${form.name.trim()}\nEmail: ${form.email.trim()}\n\nСообщение:\n${form.message.trim()}`,
  )
  window.location.href = `mailto:${person.email}?subject=${subject}&body=${body}`

  isSent.value = true
  form.name = ''
  form.email = ''
  form.message = ''
}

const contacts = [
  {
    icon: Mail,
    label: 'Email',
    value: person.email,
    href: `mailto:${person.email}`,
  },
  {
    icon: Phone,
    label: 'Телефон',
    value: person.phone,
    href: person.phoneHref,
  },
  {
    icon: MapPin,
    label: 'Город',
    value: person.city,
    href: '',
  },
  {
    icon: Clock,
    label: 'Часы работы',
    value: person.workHours,
    href: '',
  },
]
</script>

<template>
  <section
    id="contact"
    class="relative scroll-mt-20 overflow-hidden bg-slate-100/60 py-20 dark:bg-white/[0.02] sm:py-28"
    aria-label="Контакты"
  >
    <GhostTitle text="КОНТАКТЫ" />
    <div class="section-container relative">
      <SectionTitle
        title="Контакты"
        subtitle="Расскажите о своём проекте — отвечу в течение дня"
        index="06"
        tag="контакты"
      />

      <div class="grid gap-10 lg:grid-cols-2 lg:gap-14">
        <!-- Форма -->
        <div ref="formBlock" class="reveal-left">
          <Card :hover="false">
            <form class="relative" novalidate @submit.prevent="submitForm">
              <div class="space-y-6">
                <div>
                  <div class="field-ring" :style="errors.name ? { background: '#f87171' } : {}">
                    <div class="field-inner relative bg-white dark:bg-ink-900">
                      <input
                        id="contact-name"
                        v-model="form.name"
                        type="text"
                        name="name"
                        autocomplete="name"
                        placeholder=" "
                        class="peer w-full bg-transparent px-4 py-3.5 text-sm outline-none placeholder-transparent"
                        :aria-invalid="!!errors.name"
                        aria-describedby="contact-name-error"
                      />
                      <label for="contact-name" class="floating-label">
                        Имя <span class="text-red-500" aria-hidden="true">*</span>
                      </label>
                    </div>
                  </div>
                  <p
                    v-if="errors.name"
                    id="contact-name-error"
                    class="mt-1.5 text-xs text-red-500"
                    role="alert"
                  >
                    {{ errors.name }}
                  </p>
                </div>

                <div>
                  <div class="field-ring" :style="errors.email ? { background: '#f87171' } : {}">
                    <div class="field-inner relative bg-white dark:bg-ink-900">
                      <input
                        id="contact-email"
                        v-model="form.email"
                        type="email"
                        name="email"
                        autocomplete="email"
                        placeholder=" "
                        class="peer w-full bg-transparent px-4 py-3.5 text-sm outline-none placeholder-transparent"
                        :aria-invalid="!!errors.email"
                        aria-describedby="contact-email-error"
                      />
                      <label for="contact-email" class="floating-label">
                        Email <span class="text-red-500" aria-hidden="true">*</span>
                      </label>
                    </div>
                  </div>
                  <p
                    v-if="errors.email"
                    id="contact-email-error"
                    class="mt-1.5 text-xs text-red-500"
                    role="alert"
                  >
                    {{ errors.email }}
                  </p>
                </div>

                <div>
                  <div class="field-ring" :style="errors.message ? { background: '#f87171' } : {}">
                    <div class="field-inner relative bg-white dark:bg-ink-900">
                      <textarea
                        id="contact-message"
                        v-model="form.message"
                        name="message"
                        rows="5"
                        placeholder=" "
                        class="peer w-full resize-y bg-transparent px-4 py-3.5 text-sm outline-none placeholder-transparent"
                        :aria-invalid="!!errors.message"
                        aria-describedby="contact-message-error"
                      />
                      <label for="contact-message" class="floating-label">
                        Сообщение <span class="text-red-500" aria-hidden="true">*</span>
                      </label>
                    </div>
                  </div>
                  <p
                    v-if="errors.message"
                    id="contact-message-error"
                    class="mt-1.5 text-xs text-red-500"
                    role="alert"
                  >
                    {{ errors.message }}
                  </p>
                </div>

                <Button type="submit" magnetic class="w-full" aria-label="Отправить сообщение">
                  <Send class="h-5 w-5" aria-hidden="true" />
                  Отправить сообщение
                </Button>

                <p v-if="isSent" class="text-center text-sm text-green-500" role="status">
                  Открылось окно почтового клиента — письмо готово к отправке. Спасибо!
                </p>

                <p class="text-center text-xs text-slate-400 dark:text-slate-500">
                  Форма откроет ваш почтовый клиент с заполненным письмом
                </p>
              </div>
            </form>
          </Card>
        </div>

        <!-- Контактная информация -->
        <div ref="infoBlock" class="reveal-right space-y-5">
          <a
            :href="person.telegram"
            target="_blank"
            rel="noopener noreferrer"
            class="group flex items-center justify-center gap-3 rounded-2xl bg-gradient-to-r from-primary to-accent bg-[length:150%_150%] px-6 py-5 text-lg font-bold text-white shadow-xl shadow-primary/30 transition-all duration-500 hover:-translate-y-1 hover:bg-[position:100%_50%] hover:shadow-2xl hover:shadow-primary/40"
          >
            <Send
              class="h-6 w-6 transition-transform duration-300 group-hover:translate-x-1 group-hover:-translate-y-0.5"
              aria-hidden="true"
            />
            Написать в Telegram
          </a>

          <Card :hover="false" spotlight>
            <ul class="relative space-y-5">
              <li
                v-for="contact in contacts"
                :key="contact.label"
                class="group/item flex items-center gap-4"
              >
                <span
                  class="rounded-xl bg-primary/10 p-3 text-primary transition-all duration-300 group-hover/item:scale-110 group-hover/item:bg-gradient-to-br group-hover/item:from-primary group-hover/item:to-accent group-hover/item:text-white"
                  aria-hidden="true"
                >
                  <component :is="contact.icon" class="h-5 w-5" />
                </span>
                <div>
                  <p
                    class="text-xs font-medium uppercase tracking-wide text-slate-400 dark:text-slate-500"
                  >
                    {{ contact.label }}
                  </p>
                  <a
                    v-if="contact.href"
                    :href="contact.href"
                    class="link-underline font-medium transition-colors hover:text-primary"
                  >
                    {{ contact.value }}
                  </a>
                  <p v-else class="font-medium">{{ contact.value }}</p>
                </div>
              </li>
            </ul>
          </Card>
        </div>
      </div>
    </div>
  </section>
</template>
