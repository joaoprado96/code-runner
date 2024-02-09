import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';

@Component({
  selector: 'app-dialog-error',
  template: `
    <h2>Erro</h2>
    <p>{{ data.mensagem }}</p>
    <p>Monitor: {{ data.monitor }}</p>
  `,
})
export class DialogErrorComponent {
  constructor(@Inject(MAT_DIALOG_DATA) public data: { mensagem: string; monitor: string }) {}
}