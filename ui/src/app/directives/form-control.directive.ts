import {
    Directive,
    OnDestroy,
    ElementRef,
    Renderer2,
    inject
  } from '@angular/core';
  import { NgControl } from '@angular/forms';
import { ValidationErrorService } from '../services/validation-error.service';
  
@Directive({
  selector: '[formControlName]',
  standalone: true
})
export class FormControlDirective implements OnDestroy {
  private control = inject(NgControl);
  private host = inject(ElementRef<HTMLElement>);
  private renderer = inject(Renderer2);
  private validationErrorService = inject(ValidationErrorService);

  private errorContainer?: HTMLElement;

  private lastDirty = false;
  private lastTouched = false;
  private lastInvalid = false;

  ngDoCheck(): void {
    const ctrl = this.control.control;
    if (!ctrl) return;

    const shouldShow =
      ctrl.invalid && (ctrl.dirty || ctrl.touched);

    const dirtyChanged = ctrl.dirty !== this.lastDirty;
    const touchedChanged = ctrl.touched !== this.lastTouched;
    const invalidChanged = ctrl.invalid !== this.lastInvalid;

    if (shouldShow && (dirtyChanged || touchedChanged || invalidChanged)) {
      this.showErrors(ctrl.errors!);
    }

    if (!shouldShow && (dirtyChanged || touchedChanged || invalidChanged)) {
      this.removeErrorContainer();
    }

    // Update tracking
    this.lastDirty = ctrl.dirty;
    this.lastTouched = ctrl.touched;
    this.lastInvalid = ctrl.invalid;
  }

  private showErrors(errors: any) {
    this.removeErrorContainer();

    const errorDiv = this.renderer.createElement('div');
    this.renderer.addClass(errorDiv, 'p-error');
    this.renderer.addClass(errorDiv, 'text-red-500');
    this.renderer.addClass(errorDiv, 'input-error-message');
    this.renderer.setStyle(errorDiv, 'font-size', '0.8rem');
    this.renderer.setStyle(errorDiv, 'margin-top', '0.25rem');

    const messages: string[] = [];
    for(let key in errors) {
      messages.push(this.validationErrorService.getError(key, errors));
    }

    for (const msg of messages) {
      const small = this.renderer.createElement('small');
      const text = this.renderer.createText(msg);
      this.renderer.appendChild(small, text);
      this.renderer.appendChild(errorDiv, small);
      if(!this.control.control?.dirty) {
        this.control.control?.markAsDirty();
      }
    }

    const next = this.host.nativeElement.nextSibling;
    const parent = this.host.nativeElement.parentNode;
    this.renderer.insertBefore(parent, errorDiv, next);
    this.errorContainer = errorDiv;
  }

  private removeErrorContainer() {
    if (this.errorContainer && this.errorContainer.parentNode) {
      this.renderer.removeChild(this.errorContainer.parentNode, this.errorContainer);
      this.errorContainer = undefined;
    }
  }

  ngOnDestroy(): void {
    this.removeErrorContainer();
  }
}