<template>
  <div class="h-full w-full bg-fantasy-dark flex flex-col">
    <!-- Header -->
    <header class="bg-fantasy-medium border-b border-fantasy-accent p-4 shadow-lg">
      <div class="container mx-auto">
        <h1 class="text-3xl font-bold text-fantasy-gold">🐉 Agents & Dragons</h1>
        <p class="text-gray-400 text-sm mt-1">AI-Powered Narrative Roleplaying Game</p>
      </div>
    </header>

    <!-- Main Chat Area -->
    <div class="flex-1 overflow-hidden">
      <div class="container mx-auto h-full flex flex-col py-4 px-4">
        <!-- Messages Container -->
        <div 
          ref="messagesContainer" 
          class="flex-1 overflow-y-auto space-y-4 mb-4 px-2"
        >
          <div 
            v-for="(message, index) in messages" 
            :key="index"
            class="animate-fade-in"
          >
            <!-- User Message -->
            <div 
              v-if="message.role === 'user'" 
              class="flex justify-end"
            >
              <div class="max-w-3xl bg-fantasy-highlight rounded-lg p-4 shadow-md">
                <div class="flex items-start gap-3">
                  <div class="flex-1">
                    <p class="text-sm font-semibold text-fantasy-gold mb-1">You</p>
                    <p class="text-white">{{ message.content }}</p>
                  </div>
                  <span class="text-2xl">⚔️</span>
                </div>
              </div>
            </div>

            <!-- Assistant Message -->
            <div 
              v-else 
              class="flex justify-start"
            >
              <div class="max-w-3xl bg-fantasy-accent rounded-lg p-4 shadow-md">
                <div class="flex items-start gap-3">
                  <span class="text-2xl">📜</span>
                  <div class="flex-1">
                    <p class="text-sm font-semibold text-fantasy-gold mb-1">Storyteller</p>
                    <div 
                      class="text-gray-200 prose prose-invert prose-sm max-w-none"
                      v-html="renderMarkdown(message.content)"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Typing Indicator -->
          <div v-if="isTyping" class="flex justify-start animate-fade-in">
            <div class="max-w-3xl bg-fantasy-accent rounded-lg p-4 shadow-md">
              <div class="flex items-start gap-3">
                <span class="text-2xl">📜</span>
                <div class="flex space-x-2">
                  <div class="w-2 h-2 bg-fantasy-gold rounded-full animate-bounce" style="animation-delay: 0s"></div>
                  <div class="w-2 h-2 bg-fantasy-gold rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                  <div class="w-2 h-2 bg-fantasy-gold rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Input Area -->
        <div class="bg-fantasy-medium rounded-lg p-4 shadow-lg">
          <form @submit.prevent="sendMessage" class="flex gap-3">
            <input
              v-model="inputMessage"
              type="text"
              placeholder="Type your action or speak to the world..."
              class="flex-1 bg-fantasy-dark text-white rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-fantasy-gold placeholder-gray-500"
              :disabled="isTyping"
            />
            <button
              type="submit"
              :disabled="!inputMessage.trim() || isTyping"
              class="bg-fantasy-gold hover:bg-opacity-80 text-white font-bold py-3 px-6 rounded-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Send
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, nextTick, onMounted } from 'vue'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

export default {
  name: 'App',
  setup() {
    const messages = ref([
      {
        role: 'assistant',
        content: `# Welcome, Adventurer!

You find yourself at the entrance of a mysterious dungeon. The ancient stone archway looms before you, covered in strange runes that seem to pulse with a faint, otherworldly light.

**What would you like to do?**

*You can:*
- Examine the runes more closely
- Enter the dungeon
- Look around the area
- Or describe any other action you'd like to take`
      }
    ])
    
    const inputMessage = ref('')
    const isTyping = ref(false)
    const messagesContainer = ref(null)

    // Configure marked for better rendering
    marked.setOptions({
      breaks: true,
      gfm: true
    })

    const renderMarkdown = (content) => {
      const rawMarkup = marked.parse(content)
      return DOMPurify.sanitize(rawMarkup)
    }

    const scrollToBottom = () => {
      nextTick(() => {
        if (messagesContainer.value) {
          messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
        }
      })
    }

    const sendMessage = async () => {
      if (!inputMessage.value.trim() || isTyping.value) return

      const userMessage = inputMessage.value.trim()
      messages.value.push({
        role: 'user',
        content: userMessage
      })
      
      inputMessage.value = ''
      scrollToBottom()
      isTyping.value = true

      try {
        // TODO: Replace with actual API call to orchestrator
        const response = await fetch('/api/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            message: userMessage,
            history: messages.value
          })
        })

        if (!response.ok) {
          throw new Error('Failed to get response from server')
        }

        const data = await response.json()
        
        messages.value.push({
          role: 'assistant',
          content: data.response
        })
      } catch (error) {
        console.error('Error sending message:', error)
        
        // Fallback demo response
        messages.value.push({
          role: 'assistant',
          content: `**[Demo Mode]**

You ${userMessage.toLowerCase()}.

The air grows colder as you proceed. In the dim light, you notice:
- Ancient torches flickering along the walls
- The sound of dripping water echoing from deeper within
- A faint smell of sulfur

*Roll for perception to notice more details, or tell me what you'd like to do next.*`
        })
      } finally {
        isTyping.value = false
        scrollToBottom()
      }
    }

    onMounted(() => {
      scrollToBottom()
    })

    return {
      messages,
      inputMessage,
      isTyping,
      messagesContainer,
      renderMarkdown,
      sendMessage
    }
  }
}
</script>

<style scoped>
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fade-in 0.3s ease-out;
}

/* Custom scrollbar */
:deep(.overflow-y-auto)::-webkit-scrollbar {
  width: 8px;
}

:deep(.overflow-y-auto)::-webkit-scrollbar-track {
  background: #16213e;
  border-radius: 4px;
}

:deep(.overflow-y-auto)::-webkit-scrollbar-thumb {
  background: #533483;
  border-radius: 4px;
}

:deep(.overflow-y-auto)::-webkit-scrollbar-thumb:hover {
  background: #e94560;
}

/* Markdown prose styling */
:deep(.prose) {
  color: #e5e7eb;
}

:deep(.prose h1),
:deep(.prose h2),
:deep(.prose h3) {
  color: #e94560;
}

:deep(.prose strong) {
  color: #f3f4f6;
  font-weight: 600;
}

:deep(.prose em) {
  color: #d1d5db;
}

:deep(.prose ul),
:deep(.prose ol) {
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
}

:deep(.prose code) {
  background-color: #1a1a2e;
  padding: 0.125rem 0.25rem;
  border-radius: 0.25rem;
  color: #e94560;
}
</style>
