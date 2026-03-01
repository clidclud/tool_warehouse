<template>
  <div class="app">
    <div class="container">
      <h1>Склад инструментов</h1>
      
      <!-- Форма добавления/редактирования -->
      <div class="form-container">
        <h2>{{ editingId ? 'Редактирование' : 'Добавление' }} записи</h2>
        <form @submit.prevent="saveItem">
          <div class="form-group">
            <label>Номенклатура:</label>
            <input 
              v-model="form.nomenclature" 
              type="text" 
              required
              placeholder="Введите наименование"
            >
          </div>
          
          <div class="form-group">
            <label>Единица измерения:</label>
            <input 
              v-model="form.unit" 
              type="text" 
              required
              placeholder="шт, кг, м и т.д."
              maxlength="10"
            >
          </div>
          
          <div class="form-group">
            <label>Количество:</label>
            <input 
              v-model="form.quantity" 
              type="number" 
              step="0.01" 
              required
              placeholder="0.00"
            >
          </div>
          
          <div class="form-actions">
            <button type="submit" class="btn btn-primary">
              {{ editingId ? 'Обновить' : 'Добавить' }}
            </button>
            <button 
              v-if="editingId" 
              type="button" 
              class="btn btn-secondary" 
              @click="cancelEdit"
            >
              Отмена
            </button>
          </div>
        </form>
      </div>

      <!-- Поиск -->
      <div class="search-container">
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Поиск по номенклатуре..."
          class="search-input"
        >
      </div>

      <!-- Таблица с данными -->
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Номенклатура</th>
              <th>Единица</th>
              <th>Количество</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in filteredItems" :key="item.id">
              <td>{{ item.id }}</td>
              <td>{{ item.nomenclature }}</td>
              <td>{{ item.unit }}</td>
              <td>{{ item.quantity }}</td>
              <td class="actions">
                <button @click="editItem(item)" class="btn-edit" title="Редактировать">✏️</button>
                <button @click="deleteItem(item.id)" class="btn-delete" title="Удалить">🗑️</button>
              </td>
            </tr>
            <tr v-if="filteredItems.length === 0">
              <td colspan="5" class="no-data">Нет данных</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'App',
  setup() {
    // Состояние
    const items = ref([])
    const editingId = ref(null)
    const searchQuery = ref('')
    const apiUrl = '/api/'
    
    // Форма
    const form = reactive({
      nomenclature: '',
      unit: '',
      quantity: ''
    })

    // Вычисляемые свойства
    const filteredItems = computed(() => {
      if (!searchQuery.value) {
        return items.value
      }
      return items.value.filter(item => 
        item.nomenclature.toLowerCase().includes(searchQuery.value.toLowerCase())
      )
    })

    // Методы
    const fetchItems = async () => {
      try {
        const response = await axios.get(apiUrl)
        items.value = response.data
      } catch (error) {
        console.error('Ошибка при загрузке данных:', error)
        alert('Ошибка при загрузке данных')
      }
    }

    const saveItem = async () => {
      try {
        if (editingId.value) {
          // Обновление существующей записи
          await axios.put(`${apiUrl}${editingId.value}/`, form)
          alert('Запись успешно обновлена')
        } else {
          // Добавление новой записи
          await axios.post(apiUrl, form)
          alert('Запись успешно добавлена')
        }
        
        resetForm()
        await fetchItems()
      } catch (error) {
        console.error('Ошибка при сохранении:', error)
        alert('Ошибка при сохранении данных')
      }
    }

    const editItem = (item) => {
      editingId.value = item.id
      form.nomenclature = item.nomenclature
      form.unit = item.unit
      form.quantity = item.quantity
    }

    const deleteItem = async (id) => {
      if (confirm('Вы уверены, что хотите удалить эту запись?')) {
        try {
          await axios.delete(`${apiUrl}${id}/`)
          alert('Запись успешно удалена')
          await fetchItems()
        } catch (error) {
          console.error('Ошибка при удалении:', error)
          alert('Ошибка при удалении данных')
        }
      }
    }

    const cancelEdit = () => {
      resetForm()
    }

    const resetForm = () => {
      form.nomenclature = ''
      form.unit = ''
      form.quantity = ''
      editingId.value = null
    }

    // Загрузка данных при монтировании компонента
    onMounted(() => {
      fetchItems()
    })

    return {
      items,
      form,
      editingId,
      searchQuery,
      filteredItems,
      fetchItems,
      saveItem,
      editItem,
      deleteItem,
      cancelEdit,
      resetForm
    }
  }
}
</script>

<style scoped>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.app {
  font-family: Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
  font-size: 2.5em;
}

.form-container {
  background-color: white;
  padding: 25px;
  border-radius: 10px;
  margin-bottom: 30px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.form-container h2 {
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 1.5em;
  color: #444;
  border-bottom: 2px solid #4CAF50;
  padding-bottom: 10px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: #555;
  font-size: 14px;
}

.form-group input {
  width: 100%;
  padding: 10px 12px;
  border: 2px solid #e0e0e0;
  border-radius: 6px;
  font-size: 15px;
  transition: all 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
}

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 10px;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 15px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-primary {
  background-color: #4CAF50;
  color: white;
}

.btn-primary:hover {
  background-color: #45a049;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(76, 175, 80, 0.3);
}

.btn-secondary {
  background-color: #f44336;
  color: white;
}

.btn-secondary:hover {
  background-color: #da190b;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(244, 67, 54, 0.3);
}

.search-container {
  margin-bottom: 25px;
}

.search-input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 15px;
  transition: all 0.3s ease;
  background-color: white;
}

.search-input:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
}

.table-container {
  background-color: white;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  background-color: #4CAF50;
  color: white;
  padding: 15px;
  text-align: left;
  font-weight: 600;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

td {
  padding: 15px;
  border-bottom: 1px solid #e0e0e0;
  color: #333;
}

tr:last-child td {
  border-bottom: none;
}

tr:hover {
  background-color: #f9f9f9;
}

.actions {
  display: flex;
  gap: 10px;
}

.btn-edit, .btn-delete {
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.3s ease;
}

.btn-edit {
  background-color: #2196F3;
  color: white;
}

.btn-edit:hover {
  background-color: #1976D2;
  transform: scale(1.1);
}

.btn-delete {
  background-color: #f44336;
  color: white;
}

.btn-delete:hover {
  background-color: #da190b;
  transform: scale(1.1);
}

.no-data {
  text-align: center;
  color: #999;
  padding: 40px;
  font-size: 16px;
}

@media (max-width: 768px) {
  .container {
    padding: 15px;
  }
  
  h1 {
    font-size: 2em;
  }
  
  table {
    font-size: 14px;
  }
  
  th, td {
    padding: 10px;
  }
  
  .actions {
    flex-direction: column;
  }
  
  .btn-edit, .btn-delete {
    width: 100%;
  }
}

/* Анимации */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.form-container, .table-container {
  animation: fadeIn 0.5s ease-out;
}
</style>