import './App.css';

import React, { useRef } from "react";
import ReactDOM from "react-dom";

import Editor from "@monaco-editor/react";

function App() {

  const editorRef = useRef(null);

  function handleEditorDidMount(editor, monaco) {
    editorRef.current = editor;
  }

  function showValue() {
    alert(editorRef.current.getValue());
  }

  function ejecutar() {
    var obj = { 'codigo': editorRef.current.getValue() }

    fetch(`http://localhost:5000/ejecutar`, {
      method: 'POST',
      body: JSON.stringify(obj),
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      }
    })
      .then(res => res.json())
      .catch(err => {
        console.error('Error:', err)
        alert("Ocurrio un error, ver la consola")
      })
      .then(response => {
        alert(response.Mensaje);
      })
  }

  return (
    <div className="App">
      <header className="App-header">

        <nav class="navbar navbar-expand-lg navbar-dark bg-dark" style={{ width: '100%' }}>
          <div class="container-fluid">
            <a class="navbar-brand" href="#">DB Rust</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
              <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
              <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                <li class="nav-item">
                  <a class="nav-link active" aria-current="page" onClick={ejecutar} style={{cursor:'pointer'}}>Ejecutar</a>
                </li>
                <li class="nav-item dropdown">
                  <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                    Reportes
                  </a>
                  <ul class="dropdown-menu">
                    <li><a class="dropdown-item" href="#">Reporte de tabla de símbolos</a></li>
                    <li><a class="dropdown-item" href="#">Reporte de errores</a></li>
                    <li><a class="dropdown-item" href="#">Reporte de base de datos existente</a></li>
                    <li><a class="dropdown-item" href="#">Reporte tablas de base de datos</a></li>
                  </ul>
                </li>
                <li class="nav-item">
                  <a class="nav-link" href="#">Acerca De</a>
                </li>
              </ul>
            </div>
          </div>
        </nav>

        <div className='row flex-grow-1' style={{ marginTop: '8%' }}>
          <Editor
            height="75vh"
            width="60vh"
            defaultValue="// Empieza con Rust"
            onMount={handleEditorDidMount}
            className={'rounded-xl'}
            theme="vs-dark"
          />
          <Editor
            height="75vh"
            width="60vh"
            theme="vs-dark"
            options={{ readOnly: true }}
          />
        </div>

      </header>
    </div>
  );
}

const rootElement = document.getElementById("root");
ReactDOM.render(<App />, rootElement);
export default App;
