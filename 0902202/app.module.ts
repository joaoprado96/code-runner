import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { MatTableModule } from '@angular/material/table';
import { MatSortModule } from '@angular/material/sort';
import { MatDialogModule } from '@angular/material/dialog';
import { MatCardModule } from '@angular/material/card';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatButtonModule } from '@angular/material/button';
import { MatAutocompleteModule } from '@angular/material/autocomplete';

import { TabelaDinamicaComponent } from './tabela-dinamica/tabela-dinamica.component';
import { CardsDinamicosComponent } from './cards-dinamicos/cards-dinamicos.component';
import { DialogErrorComponent } from './dialog-error/dialog-error.component';

// Importar outros componentes e módulos necessários...

@NgModule({
  declarations: [
    TabelaDinamicaComponent,
    CardsDinamicosComponent,
    DialogErrorComponent,
    // Outros componentes...
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    MatTableModule,
    MatSortModule,
    MatDialogModule,
    BrowserAnimationsModule,
    MatCardModule,
    FormsModule,
    ReactiveFormsModule,
    MatInputModule,
    MatSelectModule,
    MatButtonModule,
    MatAutocompleteModule,
    // Outros módulos...
  ],
  providers: [],
  bootstrap: [TabelaDinamicaComponent]
})
export class AppModule { }
