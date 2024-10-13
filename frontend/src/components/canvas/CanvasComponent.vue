<template>
  <div class="container text-center">

    <div class="row justify-content-center align-items-start">
      <!-- Video y Canvas -->
      <div class="col-lg-7 mb-4 position-relative">
        <video ref="video" class="video-fluid" src="./otro minuto.mp4" @loadeddata="adjustCanvasSize"></video>
        <canvas ref="canvas" class="position-absolute"></canvas>
      </div>

      <!-- Botones y Lista de Polígonos -->
      <div class="col-lg-3">
        <div class="mb-3 d-flex flex-column">
          <button class="btn btn-primary mb-2 btn-block" @click="finalizarPoly">Finalizar Polígono (f)</button>
          <button class="btn btn-warning mb-2 btn-block" @click="deshacerPoly">Deshacer Polígono (Ctrl-z)</button>
          <button class="btn btn-secondary mb-2 btn-block" @click="cancelarPoly">Cancelar Polígono (Esc)</button>
          <button class="btn btn-info mb-2 btn-block" @click="rehacerPoly">Rehacer Polígono (Ctrl-r)</button>
          <button class="btn btn-danger mb-2 btn-block" @click="limpiarCanvas">Limpiar Canvas</button>
          <button class="btn btn-primary mb-2 btn-block" @click="showPreview = true">Procesar</button>
        </div>

        <!-- Selector de Tipo -->
        <div class="mb-4">
          <label for="tipo" class="form-label">Tipo (t)</label>
          <select v-model="tipo" class="form-select">
            <option value="Entrada">Entrada</option>
            <option value="Salida">Salida</option>
            <option value="Exclusion">Exclusión</option>
          </select>
        </div>

        <!-- Lista de Polígonos -->
        <div v-show="polygons.length>0" class="polygon-list-container">
          <ol ref="polygonList" class="list-group">
            <li v-for="(polygon, index) in polygons" :key="index" class="list-group-item d-flex justify-content-between align-items-center">
              <span>{{ polygon.name ? polygon.name : polygon.tipo  }}</span>
              <div class="btn-group">
                <button class="btn btn-danger btn-sm" @click="eliminarPoly(index)">Eliminar (d)</button>
                <button class="btn btn-secondary btn-sm" @click="cambiarTipo(index)">Cambiar Tipo (t)</button>
                <button class="btn btn-secondary btn-sm" @click="cambiarNombre(index)">Cambiar nombre (r)</button>
              </div>
            </li>
          </ol>
        </div>
      </div>
    </div>
  </div>

  <!-- Overlay preview de poligonos -->
  <div v-if="showPreview">
    <div v-if="polygons.length > 0" class="overlay">
      <div class="overlay-content">
        <h2>Vista Previa de Polígonos</h2>
        <ol ref="polygonList" class="list-group">
          <li v-for="(polygon, index) in polygons" :key="index" class="list-group-item d-flex justify-content-between align-items-center">
            <span>{{ polygon.name ? polygon.name : polygon.tipo  }}</span>
            <span>{{ polygon.tipo }}</span>
            <div class="btn-group">
              <button class="btn btn-secondary btn-sm" @click="cambiarTipo(index)">Cambiar Tipo</button>
              <button class="btn btn-secondary btn-sm" @click="cambiarNombre(index)">Cambiar nombre</button>
            </div>
          </li>
        </ol>
        <button class="btn btn-primary mt-3" @click="processPolygons">Confirmar y Procesar</button>
        <button class="btn btn-secondary mt-3" @click="showPreview = false">Volver al canvas</button>
      </div>
    </div>
    <div v-else class="alert alert-warning" role="alert">
      Es necesario tener poligonos para procesar
      <button class="btn btn-secondary mt-3" @click="showPreview = false">Cerrar</button>
    </div>
  </div>
</template>

<script>
import { apiService } from '@/services/api';
let canvas = null;
let video = null;
let ctx = null;
let polygonList = null;
const colores = {
  Entrada: 'lightgreen',
  Salida: 'blue',
  Exclusion: 'red'
};
let oldCanvasWidth = 0;
let oldCanvasHeight = 0;
export default {
  data() {
    return {
      isDrawing: false,
      tipo: 'Entrada',
      currentPolygon: { points: [], tipo: 'Entrada', name: 'Entrada' },
      polygons: [],         // [{points: [[x,y],[x,y]...[x,y]], tipo: this.tipo}] 
      deletedPolygons: [],
      highlightedPolygonIndex: null,
      showPreview: false,
    };
  },

  methods: {
    adjustCanvasSize() {
      const videoRect = this.video.getBoundingClientRect();
      this.oldCanvasWidth = this.canvas.width;
      this.oldCanvasHeight = this.canvas.height;
      this.canvas.width = videoRect.width;
      this.canvas.height = videoRect.height;
    },

    getMousePosition(event) {
      const rect = this.canvas.getBoundingClientRect();
      return [event.clientX - rect.left, event.clientY - rect.top];
    },

    drawPolygons(polys) {
      const ctx = this.ctx;
      ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
      polys.forEach((polygon, index) => {
        ctx.beginPath();
        ctx.moveTo(polygon.points[0][0], polygon.points[0][1]);
        for (let i = 1; i < polygon.points.length; i++) {
          ctx.lineTo(polygon.points[i][0], polygon.points[i][1]);
        }
        ctx.closePath();
        ctx.strokeStyle = colores[polygon.tipo];
        ctx.lineWidth = index === this.highlightedPolygonIndex ? 2.5 : 1.5; // Aumenta el grosor si está resaltado
        ctx.stroke();
      });
    },

    cleanActualPath() {
      this.currentPolygon.points = [];
      this.isDrawing = false;
      this.drawPolygons(this.polygons);
    },

    deshacerPoly() {
      if (this.polygons.length > 0) {
        this.deletedPolygons.push(this.polygons.pop());
        this.cleanActualPath();
      }
    },

    rehacerPoly() {
      if (this.deletedPolygons.length > 0) {
        this.polygons.push(this.deletedPolygons.pop());
        this.cleanActualPath();
      }
    },

    finalizarPoly() {
      if (this.currentPolygon.points.length >= 3) {
        this.polygons.push({ points: [...this.currentPolygon.points], tipo: this.tipo, name: this.tipo });
      }
      this.cleanActualPath();
    },

    cancelarPoly() {
      this.cleanActualPath();
    },

    limpiarCanvas() {
      if (confirm("¿Estás seguro?")) {
        this.polygons = [];
        this.deletedPolygons = [];
        this.cleanActualPath();
      }
    },
    
    eliminarPoly(index) {
      this.polygons.splice(index, 1);
      this.cleanActualPath();
    },
    
    cambiarTipo(index) {
      const polygon = this.polygons[index];
      polygon.tipo = this.ciclarTipo(polygon.tipo);
      if(polygon.name in colores) //esto se da cuando no se le asigna un nombre 
        polygon.name = polygon.tipo
      this.cleanActualPath();
    },
    
    toggleTipo() {
      this.tipo = this.ciclarTipo(this.tipo);
      if(this.currentPolygon.name in colores)
        this.currentPolygon.name = this.currentPolygon.tipo
    },

    ciclarTipo(tipo) {
      const tipos = ['Entrada', 'Salida', 'Exclusion'];
      let i = tipos.indexOf(tipo);
      i = (i + 1) % tipos.length;
      return tipos[i];
    },

    highlightPolygon(index) {
      if (this.highlightedPolygonIndex !== index) {
        this.removePolygonHighlight();

        const listItem = this.polygonList.children[index];
        listItem.style.color = 'yellow';

        this.highlightedPolygonIndex = index;
        this.cleanActualPath();
      }
    },

    removePolygonHighlight() {
      if (this.highlightedPolygonIndex !== null) {
        const previousListItem = this.polygonList.children[this.highlightedPolygonIndex]
        if (previousListItem) previousListItem.style.color = '';

        this.highlightedPolygonIndex = null;
        this.cleanActualPath(); // Redibuja para quitar el resaltado
      }
    },

    isMouseInPolygon(mousePos, polygon) {
      let isInside = false;
      for (let i = 0, j = polygon.points.length - 1; i < polygon.points.length; j = i++) {
        const xi = polygon.points[i][0], yi = polygon.points[i][1];
        const xj = polygon.points[j][0], yj = polygon.points[j][1];
        const mousePosX = mousePos[0];
        const mousePosY = mousePos[1];
        
        const intersect = ((yi > mousePosY) !== (yj > mousePosY)) &&
                          (mousePosX < (xj - xi) * (mousePosY - yi) / (yj - yi) + xi);
        if (intersect) isInside = !isInside;
      }
      return isInside;
    },

    resizePolygons(oldX, oldY, newX, newY) {
      const scaleX = newX/oldX;
      const scaleY = newY/oldY;
      for(let polygon of this.polygons) {
        for(let point of polygon.points) {
          point[0] *= scaleX;
          point[1] *= scaleY;
        }
      }
      this.cleanActualPath();
    },
    
    promptForName() {
      return prompt("Ingrese el nuevo nombre del polígono:");
    },
    
    cambiarNombre(index) {
      const newName = this.promptForName();
      if (newName !== null && newName.trim() !== '') {
        this.polygons[index].name = newName;
      }
    },

    async processPolygons() {
      const x = this.canvas.width;
      const y = this.canvas.height;
      const path = "otro minuto.mp4"
      let data = {polygons: this.polygons.map(p => ({ tipo: p.tipo, points: p.points, name: p.name })), res: [x,y], path: path};
      this.showPreview = false;
      try {
        const response = await apiService.post("modelo/encolar", data);
        if(response.status == 200) {
            this.$toast.success("Se envió a procesar a la cola de procesamiento")    
        }
      } catch(error) {
        this.$toast.error(error)
      }
      this.$router.push('prueba');
    },
  },

  mounted() {
    this.polygonList = this.$refs.polygonList
    this.canvas = this.$refs.canvas;
    this.ctx = this.canvas.getContext('2d');
    this.video = this.$refs.video;

    window.addEventListener('resize', () => {      
      this.adjustCanvasSize();      
      const newX = this.canvas.width;
      const newY = this.canvas.height;
      this.resizePolygons(this.oldCanvasWidth, this.oldCanvasHeight, newX, newY);
    });

    this.canvas.addEventListener('mousedown', (event) => {
      this.isDrawing = true;
      const pos = this.getMousePosition(event);
      this.currentPolygon.points.push(pos);
    });

    this.canvas.addEventListener('mousemove', (event) => {
      const pos = this.getMousePosition(event);
      if(this.isDrawing) {
        const tempPolygon = { points: [...this.currentPolygon.points, pos], tipo: this.currentPolygon.tipo };
        this.drawPolygons([...this.polygons, tempPolygon]);
      } else {
        let polygonFound = false;

        this.polygons.forEach((polygon, index) => {
          if (this.isMouseInPolygon(pos, polygon)) {
            this.highlightPolygon(index);
            polygonFound = true;
          }
        });

        if (!polygonFound && this.highlightedPolygonIndex !== null) {
          this.removePolygonHighlight();
        }
      }
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'f') this.finalizarPoly();
      else if (e.ctrlKey && e.key === 'z') this.deshacerPoly();
      else if (e.ctrlKey && e.key === 'r') {
        e.preventDefault();
        e.stopPropagation();
        this.rehacerPoly();
      }
      else if (e.key === 'Escape') this.cancelarPoly();
      else if (e.key === 't') {
        if (this.highlightedPolygonIndex !== null) {
          this.cambiarTipo(this.highlightedPolygonIndex);
        } else this.toggleTipo();
      } else if (e.key == 'd') {
        if(this.highlightedPolygonIndex !== null){
          this.eliminarPoly(this.highlightedPolygonIndex);
        }
      } else if (e.key == 'r') {
        if(this.highlightedPolygonIndex !== null) {
          this.cambiarNombre(this.highlightedPolygonIndex);
        }
      }
    });
  },

  watch: {
    tipo() {
      this.currentPolygon.tipo = this.tipo;
    }
  }
};
</script>

<style scoped>
body {
  background-color: #2e2e2e;
  color: #f1f1f1;
  font-family: 'Arial', sans-serif;
}

h1 {
  font-size: 2.5rem;
  color: #f1f1f1;
}

.container {
  max-width: 100%; /* Asegúrate de que el contenedor ocupe el 100% de su contenedor padre */
}

.video-fluid {
  width: 100%;
  height: auto;
  border: 2px solid #ddd;
  border-radius: 5px;
}

.col-lg-7 {
  padding: 0;
  margin: 0;
}

canvas {
  top: 0;
  left: 0;
}

.list-group-item {
  background-color: #444;
  color: #f1f1f1;
  border: none;
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 5px;
}

.btn-group button {
  margin-left: 5px;
}

.btn-primary {
  background-color: #007bff;
  border: none;
}

.btn-warning {
  background-color: #ffc107;
  border: none;
}

.btn-secondary {
  background-color: #6c757d;
  border: none;
}

.btn-danger {
  background-color: #dc3545;
  border: none;
}

.btn-info {
  background-color: #17a2b8;
  border: none;
}

select.form-select {
  background-color: #444;
  color: #f1f1f1;
  border: none;
}

option {
  background-color: #444;
  color: #f1f1f1;
}
/* Para la vista previa de procesar */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.overlay-content {
  background: #387e5baf;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  max-width: 30%; /* Increased width */
  max-height: 80%; /* Added height constraint */
  width: 100%;
  overflow-y: auto; /* Added scroll for overflow content */
}

.alert-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.alert {
  max-width: 500px;
  width: 100%;
  text-align: center;
}

.polygon-list-container {
  max-height: 300px; /* Ajusta según tus necesidades */
  overflow-y: auto; /* Habilita el desplazamiento vertical */
  background-color: #444; /* Color de fondo */
  border-radius: 5px; /* Esquinas redondeadas */
  padding: 10px; /* Espaciado interno */
}
</style>
